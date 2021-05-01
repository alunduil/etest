"""Main etest module."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import logging
import signal
import sys
import threading
from typing import List

import click

from etest import docker, information, qemu, tests
from etest.profile import Profile

logger = logging.getLogger(__name__)
logger.propagate = False
logger.addHandler(logging.NullHandler())


def echo_check(check: tests.Test):
    """Print a check status."""
    if check.failed:
        click.secho("F", nl=False, fg="red")
    else:
        click.secho(".", nl=False, fg="green")


def echo_check_verbose(check: tests.Test):
    """Print a check if verbose was requested."""
    click.echo("[", nl=False)
    if check.failed:
        click.secho("!!", nl=False, fg="red")
    else:
        click.secho("OK", nl=False, fg="green")
    click.echo("] ", nl=False)

    click.echo(check.name, nl=False)

    click.echo()


@click.command()
@click.option("-d", "--dry-run", is_flag=True, default=False, help="Report actions but do not run tests.")
@click.option("-f", "--fast", is_flag=True, default=False, help="Stop at first failure.")
@click.option("-j", "--jobs", default=1, help="Number of test to run simultaneously.")
@click.option("-q", "--quiet", is_flag=True, default=False, help="Suppress all output.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Provide more output.")
@click.option("--hardened/--no-hardened", default=False, help="Use a hardened profile.")
@click.option("--multilib/--no-multilib", default=True, help="Use a multilib profile.")
@click.option("--systemd/--no-systemd", default=False, help="Use a systemd profile.")
@click.option(
    "--architecture",
    "--arch",
    type=click.Choice(["amd64", "x86", "arm64", "armv5", "armv7", "ppc64"], case_sensitive=False),
    default="amd64",
    help="Architecture for the built image.",
)
@click.option(
    "--libc",
    type=click.Choice(["glibc", "musl", "uclibc"], case_sensitive=False),
    default="glibc",
    help="libc for the built image.",
)
@click.version_option(information.VERSION)
@click.argument("ebuilds", nargs=-1)
def etest(
    dry_run: bool,
    fast: bool,
    jobs: int,
    quiet: bool,
    verbose: bool,
    hardened: bool,
    multilib: bool,
    systemd: bool,
    architecture: str,
    libc: str,
    ebuilds: List[str],
):
    """Test one or more ebuilds."""
    signal.signal(signal.SIGINT, sigint_handler)

    failures = []
    elapsed_times = []

    output_lock = threading.Lock()
    jobs_limit_sem = threading.BoundedSemaphore(value=jobs)

    profile = Profile(quiet, architecture, libc, hardened, multilib, systemd)
    profile.build()

    with qemu.qemu(profile.arch):

        def _(check):
            if not dry_run:
                check.run()

            elapsed_times.append(check.time)

            if quiet:
                pass
            elif verbose:
                with output_lock:
                    echo_check_verbose(check)
            else:
                with output_lock:
                    echo_check(check)

            if check.failed:
                failures.append(check)

            jobs_limit_sem.release()

        for check in tests.Tests(profile, ebuilds):
            jobs_limit_sem.acquire()

            if fast and len(failures):
                jobs_limit_sem.release()
                break

            threading.Thread(target=_, args=(check,)).start()

        while threading.active_count() > 1:
            threading.enumerate().pop().join()

    elapsed_time = sum(elapsed_times, datetime.timedelta())

    if not quiet:
        for check in failures:
            click.echo()
            click.echo()
            click.echo("=" * min(click.get_terminal_size()[0], 72))
            click.secho(check.name, bold=True)
            click.echo(check.failed_command)
            click.echo("-" * min(click.get_terminal_size()[0], 72))
            click.echo(check.output)
            click.echo()

        if not verbose:
            click.echo()

        click.echo("-" * min(click.get_terminal_size()[0], 72))
        click.echo(f"{len(elapsed_times)} tests ran in {elapsed_time.total_seconds()} seconds.")
        if len(failures):
            click.secho("{} tests FAILED".format(len(failures)), fg="red")

    sys.exit(len(failures))


def sigint_handler(signum, frame):
    """Interrupt signal handler."""
    docker.container.CREATE = False

    while len(docker.container.CONTAINERS):
        docker.container.stop(docker.container.CONTAINERS[0])

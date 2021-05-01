"""Main etest module."""
import datetime
import logging
import signal
import sys
import threading
from types import FrameType
from typing import Optional, Tuple

import click

from etest import docker, information, tests

logger = logging.getLogger(__name__)
logger.propagate = False
logger.addHandler(logging.NullHandler())


def echo_check(check: tests.Test) -> None:
    """Print a check status."""
    if check.failed:
        click.secho("F", nl=False, fg="red")
    else:
        click.secho(".", nl=False, fg="green")


def echo_check_verbose(check: tests.Test) -> None:
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
@click.option("-d", "--dry-run", is_flag=True, default=False, help="report actions but do not run tests")
@click.option("-f", "--fast", is_flag=True, default=False, help="stop at first failure")
@click.option("-j", "--jobs", default=1, help="number of test to run simultaneously")
@click.option("-q", "--quiet", is_flag=True, default=False, help="suppress all output")
@click.option("-v", "--verbose", is_flag=True, default=False, help="provide more output")
@click.version_option(information.VERSION)
@click.argument("ebuilds", nargs=-1)
def etest(dry_run: bool, fast: bool, jobs: int, quiet: bool, verbose: bool, ebuilds: Optional[Tuple[str]]) -> None:
    """Test one or more ebuilds."""
    signal.signal(signal.SIGINT, sigint_handler)

    failures = []
    elapsed_times = []

    output_lock = threading.Lock()
    jobs_limit_sem = threading.BoundedSemaphore(value=jobs)

    def _(check: tests.Test) -> None:
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

    for check in tests.Tests(ebuilds):
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
        click.echo("{} tests ran in {} seconds".format(len(elapsed_times), elapsed_time.total_seconds()))
        if len(failures):
            click.secho("{} tests FAILED".format(len(failures)), fg="red")

    sys.exit(len(failures))


def sigint_handler(signals: signal.Signals, frame: FrameType) -> None:
    """Interrupt signal handler."""
    docker.container.CREATE = False

    while len(docker.container.CONTAINERS):
        docker.container.stop(docker.container.CONTAINERS[0])

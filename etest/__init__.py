"""Main etest module."""
import datetime
import logging
import shutil
import signal
import sys
import threading
import typing
from types import FrameType
from typing import Optional, Tuple

import click  # pylint: disable=E0401

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


@click.command()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "-d",
    "--dry-run",
    is_flag=True,
    default=False,
    help="report actions but do not run tests",
)
@click.option("-f", "--fast", is_flag=True, default=False, help="stop at first failure")  # type: ignore[misc]
@click.option("-j", "--jobs", default=1, help="number of test to run simultaneously")  # type: ignore[misc]
@click.option("-q", "--quiet", is_flag=True, default=False, help="suppress all output")  # type: ignore[misc]
@click.option("-v", "--verbose", is_flag=True, default=False, help="provide more output")  # type: ignore[misc]
@click.version_option(information.VERSION)  # type: ignore[misc]
@click.argument("ebuilds", nargs=-1)  # type: ignore[misc]
def etest(  # pylint: disable=R0913
    dry_run: bool,
    fast: bool,
    jobs: int,
    quiet: bool,
    verbose: bool,
    ebuilds: Optional[Tuple[str]],
) -> None:
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
        jobs_limit_sem.acquire()  # pylint: disable=R1732

        if fast and failures:
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
            click.echo("=" * min(shutil.get_terminal_size()[0], 72))
            click.secho(check.name, bold=True)
            click.echo(check.failed_command)
            click.echo("-" * min(shutil.get_terminal_size()[0], 72))
            click.echo(check.output)
            click.echo()

        if not verbose:
            click.echo()

        click.echo("-" * min(shutil.get_terminal_size()[0], 72))
        click.echo(
            f"{len(elapsed_times)} tests ran in {elapsed_time.total_seconds()} seconds"
        )
        if failures:
            click.secho(f"{len(failures)} tests FAILED", fg="red")

    sys.exit(len(failures))


def sigint_handler(_signal: int, _frame: typing.Optional[FrameType] = None) -> None:
    """Interrupt signal handler."""
    docker.container.CREATE = False

    while docker.container.CONTAINERS:
        docker.container.stop(docker.container.CONTAINERS[0])

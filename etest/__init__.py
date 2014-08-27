# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import click
import datetime

from etest import information
from etest import tests


def echo_check(check):
    if check.failed:
        click.secho('F', nl = False, color = 'red')
    else:
        click.secho('·', nl = False, color = 'green')


def echo_check_verbose(check):
    click.echo('[', nl = False)
    if check.failed:
        click.secho('!!', nl = False, color = 'red')
    else:
        click.secho('OK', nl = False, color = 'green')
    click.echo('] ', nl = False)

    click.echo(check)


@click.command()
@click.option('-d', '--dry-run', is_flag = True, default = False, help = 'report actions but do not run tests')
@click.option('-f', '--fast', is_flag = True, default = False, help = 'stop at first failure')
@click.option('-j', '--jobs', default = 1, help = 'number of tests to run simultaneously')
@click.option('-q', '--quiet', is_flag = True, default = False, help = 'suppress all output')
@click.option('-v', '--verbose', is_flag = True, default = False, help = 'provide more output')
@click.version_option(information.VERSION)
@click.argument('ebuilds', nargs = -1)
def etest(dry_run, fast, jobs, quiet, verbose, ebuilds):
    checks = tests.Tests(ebuilds)
    elapsed_time = datetime.timedelta()
    failures = []

    for check in checks:
        if not dry_run:
            check.run()
            elapsed_time += check.time

        if check.failed:
            failures.append(check)

        if quiet:
            continue
        elif verbose:
            echo_check_verbose(check)
        else:
            echo_check(check)

    if not quiet:
        if verbose:
            for check in failures:
                click.echo()
                click.echo('-' * click.get_terminal_size[0])
                click.echo(check.output)
            click.echo('-' * click.get_terminal_size[0])

        click.echo()
        click.echo('-' * click.get_terminal_size[0])
        click.secho('{0} tests ran in {1} seconds'.format(len(checks)), elapsed_time.total_seconds(), color = 'green')
        if len(failures):
            click.secho('{0} tests FAILED'.format(len(failures)), color = 'red')

    return len(failures)


if __name__ == '__main__':
    etest()

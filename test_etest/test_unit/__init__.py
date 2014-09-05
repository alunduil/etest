# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import click.testing
import logging
import unittest

from etest import etest
from etest import information

logger = logging.getLogger(__name__)


class TestEtestCliStandardOptions(unittest.TestCase):
    def setUp(self):
        self.runner = click.testing.CliRunner()

    def test_etest_help(self):
        '''etest --help'''

        _ = self.runner.invoke(etest, [ '--help' ])

        logger.debug('etest --help:\n%s', _.output)

        self.assertEqual(0, _.exit_code)

    def test_etest_version(self):
        '''etest --version'''

        _ = self.runner.invoke(etest, [ '--version' ])

        logger.debug('etest --version:\n%s', _.output)

        self.assertEqual('etest, version ' + information.VERSION + '\n', _.output)

        self.assertEqual(0, _.exit_code)


class TestEtestCliEbuild(unittest.TestCase):
    def setUp(self):
        self.runner = click.testing.CliRunner()

        with self.runner.isolated_filesystem():
            pass

    def test_etest_quiet_ebuild(self):
        '''etest --quiet'''

        _ = self.runner.invoke(etest, [ '--quiet' ])

        self.assertEqual('', _.output)

        self.assertEqual(0, _.exit_code)

    def test_etest_verbose_ebuild(self):
        '''etest --verbose'''

        _ = self.runner.invoke(etest, [ '--verbose' ])

        self.assertEqual(
            '[OK] app-portage/etest\n'
            '-\n'
            '1 tests ran in 0.003 seconds\n',
            _.output
        )

        self.assertEqual(0, _.exit_code)

    def test_etest_ebuild(self):
        '''etest'''

        _ = self.runner.invoke(etest, [])

        self.assertEqual(
            '·\n'
            '-\n'
            '1 tests ran in 0.003 seconds\n',
            _.output
        )

        self.assertEqual(0, _.exit_code)

    def test_etest_specific_ebuild(self):
        '''etest app-portage/etest'''

        _ = self.runner.invoke(etest, [ 'app-portage/etest' ])

        self.assertEqual(
            '·\n'
            '-\n'
            '1 tests ran in 0.003 seconds\n',
            _.output
        )

        self.assertEqual(0, _.exit_code)

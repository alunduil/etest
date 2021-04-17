# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import click.testing
import functools
import logging
import os
import traceback
import unittest

from test_etest.test_fixtures import FIXTURES_DIRECTORY

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

        logger.debug('exception: %s', _.exception)
        logger.debug('traceback:\n%s', _.exc_info)

        self.assertEqual(0, _.exit_code)

    def test_etest_version(self):
        '''etest --version'''

        _ = self.runner.invoke(etest, [ '--version' ])

        logger.debug('etest --version:\n%s', _.output)

        logger.debug('exception: %s', _.exception)
        logger.debug('traceback:\n%s', _.exc_info)

        self.assertEqual('etest, version ' + information.VERSION + '\n', _.output)

        self.assertEqual(0, _.exit_code)


class TestEtestCliEbuild(unittest.TestCase):
    def setUp(self):
        self.runner = click.testing.CliRunner()

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(os.path.join(FIXTURES_DIRECTORY, 'overlay'))

    def test_etest_quiet_ebuild(self):
        '''etest --quiet'''

        _ = self.runner.invoke(etest, [ '--quiet' ])

        logger.debug('exception: %s', _.exception)
        logger.debug('traceback:\n%s', ''.join(traceback.format_tb(_.exc_info[2])))

        self.assertEqual('', _.output)

        self.assertEqual(0, _.exit_code)

    def test_etest_verbose_ebuild(self):
        '''etest --verbose'''

        _ = self.runner.invoke(etest, [ '--verbose' ])

        logger.debug('exception: %s', _.exception)
        logger.debug('traceback:\n%s', ''.join(traceback.format_tb(_.exc_info[2])))

        self.assertRegex(
            _.output,
            r'\[OK\] =app-portage/etest-9999\[\]\n'
            r'\[OK\] =app-portage/etest-9999\[test\]\n'
            r'-+\n'
            r'2 tests ran in \d+(?:\.\d+)? seconds\n'
        )

        self.assertEqual(0, _.exit_code)

    def test_etest_parallel_ebuild(self):
        '''etest -j2'''

        _ = self.runner.invoke(etest, [ '-j', '2' ])

        logger.debug('exception: %s', _.exception)
        logger.debug('traceback:\n%s', ''.join(traceback.format_tb(_.exc_info[2])))

        self.assertRegex(
            _.output,
            r'··\n'
            r'-+\n'
            r'2 tests ran in \d+(?:\.\d+)? seconds\n'
        )

        self.assertEqual(0, _.exit_code)

    def test_etest_ebuild(self):
        '''etest'''

        _ = self.runner.invoke(etest, [])

        logger.debug('exception: %s', _.exception)
        logger.debug('traceback:\n%s', ''.join(traceback.format_tb(_.exc_info[2])))

        self.assertRegex(
            _.output,
            r'··\n'
            r'-+\n'
            r'2 tests ran in \d+(?:\.\d+)? seconds\n'
        )

        self.assertEqual(0, _.exit_code)

    def test_etest_specific_ebuild(self):
        '''etest app-portage/etest'''

        _ = self.runner.invoke(etest, [ 'app-portage/etest' ])

        logger.debug('exception: %s', _.exception)
        logger.debug('traceback:\n%s', ''.join(traceback.format_tb(_.exc_info[2])))

        self.assertRegex(
            _.output,
            r'··\n'
            r'-+\n'
            r'2 tests ran in \d+(?:\.\d+)? seconds\n'
        )

        self.assertEqual(0, _.exit_code)

# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import click.testing
import logging
import os
import shutil
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

    def populate_cd_with_overlay(self):
        logger.debug('ls: %s', os.listdir())

        _ = os.path.join(FIXTURES_DIRECTORY, 'overlay')

        for dirent in os.listdir(_):
            logger.debug('dirent: %s', dirent)

            if os.path.isdir(os.path.join(_, dirent)):
                shutil.copytree(os.path.join(_, dirent), dirent)

        logger.debug('ls: %s', os.listdir())

    def test_etest_quiet_ebuild(self):
        '''etest --quiet'''

        with self.runner.isolated_filesystem():
            self.populate_cd_with_overlay()

            _ = self.runner.invoke(etest, [ '--quiet' ])

        logger.debug('exception: %s', _.exception)
        logger.debug('traceback:\n%s', ''.join(traceback.format_tb(_.exc_info[2])))

        self.assertEqual('', _.output)

        self.assertEqual(0, _.exit_code)

    def test_etest_verbose_ebuild(self):
        '''etest --verbose'''

        with self.runner.isolated_filesystem():
            self.populate_cd_with_overlay()

            _ = self.runner.invoke(etest, [ '--verbose' ])

        logger.debug('exception: %s', _.exception)
        logger.debug('traceback:\n%s', ''.join(traceback.format_tb(_.exc_info[2])))

        self.assertEqual(
            '[OK] app-portage/etest\n'
            '-\n'
            '1 tests ran in 0.003 seconds\n',
            _.output
        )

        self.assertEqual(0, _.exit_code)

    def test_etest_ebuild(self):
        '''etest'''

        with self.runner.isolated_filesystem():
            self.populate_cd_with_overlay()

            _ = self.runner.invoke(etest, [])

        logger.debug('exception: %s', _.exception)
        logger.debug('traceback:\n%s', ''.join(traceback.format_tb(_.exc_info[2])))

        self.assertEqual(
            '·\n'
            '-\n'
            '1 tests ran in 0.003 seconds\n',
            _.output
        )

        self.assertEqual(0, _.exit_code)

    def test_etest_specific_ebuild(self):
        '''etest app-portage/etest'''

        with self.runner.isolated_filesystem():
            self.populate_cd_with_overlay()

            _ = self.runner.invoke(etest, [ 'app-portage/etest' ])

        logger.debug('exception: %s', _.exception)
        logger.debug('traceback:\n%s', ''.join(traceback.format_tb(_.exc_info[2])))

        self.assertEqual(
            '·\n'
            '-\n'
            '1 tests ran in 0.003 seconds\n',
            _.output
        )

        self.assertEqual(0, _.exit_code)

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


class TestEtestCli(unittest.TestCase):
    def setUp(self):
        self.runner = click.testing.CliRunner()

    def test_etest_help(self):
        _ = self.runner.invoke(etest, [ '--help' ])

        logger.debug('etest --help:\n%s', _.output)

        self.assertEqual(0, _.exit_code)

    def test_etest_version(self):
        _ = self.runner.invoke(etest, [ '--version' ])

        logger.debug('etest --version:\n%s', _.output)

        self.assertEqual('etest, version ' + information.VERSION + '\n', _.output)

        self.assertEqual(0, _.exit_code)

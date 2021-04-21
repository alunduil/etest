"""Etest command tests."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import logging
import os
import traceback
import unittest

import click.testing
import pytest

from etest import etest
from etest_test.fixtures_test import FIXTURES_DIRECTORY

logger = logging.getLogger(__name__)


class TestEtestCliEbuild(unittest.TestCase):
    """Test etest command."""

    def setUp(self):
        """Set up test cases."""
        self.runner = click.testing.CliRunner()

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(os.path.join(FIXTURES_DIRECTORY, "overlay"))

    @pytest.mark.skip("Takes far too long to run.")
    def test_etest_quiet_ebuild(self):
        """Run etest --quiet."""
        _ = self.runner.invoke(etest, ["--quiet"])

        logger.debug("exception: %s", _.exception)
        logger.debug("traceback:\n%s", "".join(traceback.format_tb(_.exc_info[2])))

        self.assertEqual("", _.output)

        self.assertEqual(0, _.exit_code)

    @pytest.mark.skip("Takes far too long to run.")
    def test_etest_verbose_ebuild(self):
        """Run etest --verbose."""
        _ = self.runner.invoke(etest, ["--verbose"])

        logger.debug("exception: %s", _.exception)
        logger.debug("traceback:\n%s", "".join(traceback.format_tb(_.exc_info[2])))

        self.assertRegex(
            _.output,
            r"\[OK\] =app-portage/etest-9999\[\]\n"
            r"\[OK\] =app-portage/etest-9999\[test\]\n"
            r"-+\n"
            r"2 tests ran in \d+(?:\.\d+)? seconds\n",
        )

        self.assertEqual(0, _.exit_code)

    @pytest.mark.skip("Fails due to mismatched output.")
    def test_etest_parallel_ebuild(self):
        """Run etest -j2."""
        _ = self.runner.invoke(etest, ["-j", "2"])

        logger.debug("exception: %s", _.exception)
        logger.debug("traceback:\n%s", "".join(traceback.format_tb(_.exc_info[2])))

        self.assertRegex(
            _.output,
            r"··\n" r"-+\n" r"2 tests ran in \d+(?:\.\d+)? seconds\n",
        )

        self.assertEqual(0, _.exit_code)

    @pytest.mark.skip("Takes far too long to run.")
    def test_etest_ebuild(self):
        """Run etest."""
        _ = self.runner.invoke(etest, [])

        logger.debug("exception: %s", _.exception)
        logger.debug("traceback:\n%s", "".join(traceback.format_tb(_.exc_info[2])))

        self.assertRegex(
            _.output,
            r"··\n" r"-+\n" r"2 tests ran in \d+(?:\.\d+)? seconds\n",
        )

        self.assertEqual(0, _.exit_code)

    @pytest.mark.skip("Takes far too long to run.")
    def test_etest_specific_ebuild(self):
        """Run etest app-portage/etest."""
        _ = self.runner.invoke(etest, ["app-portage/etest"])

        logger.debug("exception: %s", _.exception)
        logger.debug("traceback:\n%s", "".join(traceback.format_tb(_.exc_info[2])))

        self.assertRegex(
            _.output,
            r"··\n" r"-+\n" r"2 tests ran in \d+(?:\.\d+)? seconds\n",
        )

        self.assertEqual(0, _.exit_code)

"""Etest command tests."""
import functools
import logging
import os
import textwrap
import traceback
import unittest

import click.testing  # pylint: disable=E0401
import pytest  # pylint: disable=E0401

from etest import etest, information
from etest_test.fixtures_test import FIXTURES_DIRECTORY

logger = logging.getLogger(__name__)


class TestEtestCliStandardOptions(unittest.TestCase):
    """Test CLI Standard Options."""

    def setUp(self) -> None:
        """Set up test cases."""
        self.runner = click.testing.CliRunner()

    def test_etest_help(self) -> None:
        """Run etest --help."""
        _ = self.runner.invoke(etest, ["--help"])

        logger.debug("etest --help:\n%s", _.output)

        logger.debug("exception: %s", _.exception)
        logger.debug("traceback:\n%s", _.exc_info)

        self.assertEqual(0, _.exit_code)

    def test_etest_version(self) -> None:
        """Run etest --version."""
        _ = self.runner.invoke(etest, ["--version"])

        logger.debug("etest --version:\n%s", _.output)

        logger.debug("exception: %s", _.exception)
        logger.debug("traceback:\n%s", _.exc_info)

        self.assertEqual("etest, version " + information.VERSION + "\n", _.output)

        self.assertEqual(0, _.exit_code)


class TestEtestCliEbuild(unittest.TestCase):
    """Test etest command."""

    def setUp(self) -> None:
        """Set up test cases."""
        self.runner = click.testing.CliRunner()

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(os.path.join(FIXTURES_DIRECTORY, "overlay"))

    @pytest.mark.skip("Takes far too long to run.")  # type: ignore[misc]
    def test_etest_quiet_ebuild(self) -> None:
        """Run etest --quiet."""
        _ = self.runner.invoke(etest, ["--quiet"])

        logger.debug("exception: %s", _.exception)
        logger.debug("traceback:\n%s", "".join(traceback.format_tb(_.exc_info[2])))

        self.assertEqual("", _.output)

        self.assertEqual(0, _.exit_code)

    @pytest.mark.skip("Takes far too long to run.")  # type: ignore[misc]
    def test_etest_verbose_ebuild(self) -> None:
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

    @pytest.mark.skip("Fails due to mismatched output.")  # type: ignore[misc]
    def test_etest_parallel_ebuild(self) -> None:
        """Run etest -j2."""
        _ = self.runner.invoke(etest, ["-j", "2"])

        logger.debug("exception: %s", _.exception)
        logger.debug("traceback:\n%s", "".join(traceback.format_tb(_.exc_info[2])))

        self.assertRegex(
            _.output,
            textwrap.dedent(
                r"""\
                ··
                -+
                2 tests ran in \d+(?:\.\d+)? seconds
                """
            ),
        )

        self.assertEqual(0, _.exit_code)

    @pytest.mark.skip("Takes far too long to run.")  # type: ignore[misc]
    def test_etest_ebuild(self) -> None:
        """Run etest."""
        _ = self.runner.invoke(etest, [])

        logger.debug("exception: %s", _.exception)
        logger.debug("traceback:\n%s", "".join(traceback.format_tb(_.exc_info[2])))

        self.assertRegex(
            _.output,
            textwrap.dedent(
                r"""\
                ··
                -+
                2 tests ran in \d+(?:\.\d+)? seconds
                """
            ),
        )

        self.assertEqual(0, _.exit_code)

    @pytest.mark.skip("Takes far too long to run.")  # type: ignore[misc]
    def test_etest_specific_ebuild(self) -> None:
        """Run etest app-portage/etest."""
        _ = self.runner.invoke(etest, ["app-portage/etest"])

        logger.debug("exception: %s", _.exception)
        logger.debug("traceback:\n%s", "".join(traceback.format_tb(_.exc_info[2])))

        self.assertRegex(
            _.output,
            textwrap.dedent(
                r"""\
                ··
                -+
                2 tests ran in \d+(?:\.\d+)? seconds
                """
            ),
        )

        self.assertEqual(0, _.exit_code)

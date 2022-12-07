"""Etest command tests."""
import logging

import click.testing  # pylint: disable=E0401

from etest import etest, information

_LOGGER = logging.getLogger(__name__)


class TestEtestCliStandardOptions:
    """Test CLI Standard Options."""

    def test_etest_help(self, cli_runner: click.testing.CliRunner) -> None:
        """Run etest --help."""
        result = cli_runner.invoke(etest, ["--help"])

        _LOGGER.debug("etest --help:\n%s", result.output)

        _LOGGER.debug("exception: %s", result.exception)
        _LOGGER.debug("traceback:\n%s", result.exc_info)

        assert result.exit_code == 0  # nosec

    def test_etest_version(self, cli_runner: click.testing.CliRunner) -> None:
        """Run etest --version."""
        result = cli_runner.invoke(etest, ["--version"])

        _LOGGER.debug("etest --version:\n%s", result.output)

        _LOGGER.debug("exception: %s", result.exception)
        _LOGGER.debug("traceback:\n%s", result.exc_info)

        assert result.output == f"etest, version {information.VERSION}\n"  # nosec

        assert result.exit_code == 0  # nosec

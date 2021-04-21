"""etest tests."""

import re

import click.testing

import etest as sut


def test_help() -> None:
    """Ensure help runs successfully."""
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.etest, ["--help"])
    assert result.exit_code == 0


def test_version() -> None:
    """Ensure version prints."""
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.etest, ["--version"])
    assert re.match(r"etest, version \d+\.\d+\.\d+\n", result.output)
    assert result.exit_code == 0

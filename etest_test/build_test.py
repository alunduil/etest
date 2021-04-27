"""Tests for etest.build."""

import click.testing

import etest.build as sut


def test_help() -> None:
    """Ensure etest-build --help exits successfully."""
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--help"])
    assert result.exit_code == 0

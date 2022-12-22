"""Tests for etest.build."""

import itertools
from unittest.mock import MagicMock, patch

import click.testing
import docker
import pytest

import etest.build as sut

sink_mock = MagicMock()


# Note for future me: Python decorators are applied from the bottom up


@patch("etest.build.docker.container.remove")
@patch("etest.build.docker.image.remove")
@patch("etest.build.docker.container.commit")
@patch("etest.build.docker.container.run")
@patch("etest.build.docker.image.build")
def test_nobuild(
    build_mock: MagicMock,
    run_mock: MagicMock,
    commit_mock: MagicMock,
    image_remove_mock: MagicMock,
    container_remove_mock: MagicMock,
) -> None:
    """Ensure that calling with --no-build actually skips builds."""
    # Run the program
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--no-build", "--verbosity", "DEBUG"])

    # Check for errors
    assert result.exit_code == 0  # nosec

    # Assert all functions have not been called
    build_mock.assert_not_called()
    run_mock.assert_not_called()
    commit_mock.assert_not_called()
    image_remove_mock.assert_not_called()
    container_remove_mock.assert_not_called()


@patch("etest.build.docker.pull", new=sink_mock)
@patch("etest.build.docker.container.create", new=sink_mock)
@patch("etest.build.docker.container.remove")
@patch("etest.build.docker.image.remove")
@patch("etest.build.docker.container.commit")
@patch("etest.build.docker.container.run")
@patch("etest.build.docker.image.build")
@pytest.mark.parametrize("arch", ["amd64", "x86", "armv5", "armv7", "arm64", "ppc64"])
def test_base_build(  # pylint: disable=too-many-arguments
    build_mock: MagicMock,
    run_mock: MagicMock,
    commit_mock: MagicMock,
    image_remove_mock: MagicMock,
    container_remove_mock: MagicMock,
    arch: str,
) -> None:
    """Ensure the base images build correctly."""
    # Run the program
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--arch", arch, "--verbosity", "DEBUG"])

    # Check for errors
    assert result.exit_code == 0  # nosec

    # Assert all functions have been called
    build_mock.assert_called_once()
    run_mock.assert_called_once()
    commit_mock.assert_called_once()
    image_remove_mock.assert_called()
    container_remove_mock.assert_called()


@patch("etest.build.docker.container.remove")
@patch("etest.build.docker.image.remove")
@patch("etest.build.docker.container.commit")
@patch("etest.build.docker.container.run")
@patch("etest.build.docker.image.build")
@pytest.mark.parametrize("libc", ["glibc", "musl", "uclibc"])
@pytest.mark.parametrize("hardened_option", ["--hardened", "--no-hardened"])
def test_alternate_libc_build(  # pylint: disable=too-many-arguments
    build_mock: MagicMock,
    run_mock: MagicMock,
    commit_mock: MagicMock,
    image_remove_mock: MagicMock,
    container_remove_mock: MagicMock,
    libc: str,
    hardened_option: str,
) -> None:
    """Ensure images with alternate libcs build correctly."""
    # Run the program
    runner = click.testing.CliRunner()
    result = runner.invoke(
        sut.main, ["--libc", libc, hardened_option, "--verbosity", "DEBUG"]
    )

    # Check for errors
    assert result.exit_code == 0  # nosec

    # Assert all functions have been called
    build_mock.assert_called_once()
    run_mock.assert_called_once()
    commit_mock.assert_called_once()
    image_remove_mock.assert_called_once()
    container_remove_mock.assert_called_once()


def test_help() -> None:
    """Ensure etest-build --help exits successfully."""
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--help"])

    assert result.exit_code == 0  # nosec


def test_builderror() -> None:
    """Ensure the program fails on a BuildError."""
    # Raise a ContainerError
    log = itertools.tee({"error": "mockup"})[0]
    error = docker.errors.BuildError(reason="Mockup error.", build_log=log)

    with patch("etest.build.docker.image.build", side_effect=error) as build_mock:
        # Run the program
        runner = click.testing.CliRunner()
        result = runner.invoke(sut.main, ["--verbosity", "DEBUG"])

        # Check if it triggered an error
        assert result.exit_code == 1  # nosec

        # Assert all functions have been called
        build_mock.assert_called_once()


@patch("etest.build.docker.container.remove")
@patch("etest.build.docker.image.remove")
@patch("etest.build.docker.image.build")
def test_cleanup(
    build_mock: MagicMock,
    image_remove_mock: MagicMock,
    container_remove_mock: MagicMock,
) -> None:
    """Ensure cleaning happens after exceptions."""
    # Raise a ContainerError
    error = docker.errors.ContainerError(
        container=True,
        exit_status=1,
        command="ls",
        image="ebuildtest/etest",
        stderr=None,
    )

    with patch("etest.build.docker.container.run", side_effect=error) as run_mock:
        # Mock cleanup functions

        # Run the program
        runner = click.testing.CliRunner()
        result = runner.invoke(sut.main, ["--verbosity", "DEBUG"])

        # Check if it triggered an error
        assert result.exit_code == 1  # nosec

        # Assert all functions have been called
        build_mock.assert_called_once()
        run_mock.assert_called_once()
        image_remove_mock.assert_called_once()
        container_remove_mock.assert_called_once()


@patch("etest.build.docker.image.push")
def test_push(push_mock: MagicMock) -> None:
    """Ensure etest-build can push."""
    # Run the program
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--no-build", "--push", "--verbosity", "DEBUG"])

    # Check for errors
    assert result.exit_code == 0  # nosec

    # Check if the program tried pushing
    assert push_mock.asssert_called_once()  # nosec

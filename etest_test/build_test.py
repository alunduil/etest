"""Tests for etest.build."""

import itertools

import click.testing
import docker
import pytest
from pytest_mock import MockerFixture

import etest.build as sut


def test_help() -> None:
    """Ensure etest-build --help exits successfully."""
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--help"])

    assert result.exit_code == 0


def test_nobuild(mocker: MockerFixture) -> None:
    """Ensure etest-build doesn't call any functions when not building."""
    # Mock build functions
    build = mocker.patch(
        "etest.build.docker.image.build",
        return_value=True,
    )
    run = mocker.patch(
        "etest.build.docker.container.run",
        return_value=True,
    )
    commit = mocker.patch("etest.build.docker.container.commit")

    # Mock cleanup functions
    image_remove = mocker.patch("etest.build.docker.image.remove")
    container_remove = mocker.patch("etest.build.docker.container.remove")

    # Run the program
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--no-build", "--verbosity", "DEBUG"])

    # Check for errors
    assert result.exit_code == 0

    # Assert all functions have not been called
    build.assert_not_called()
    run.assert_not_called()
    commit.assert_not_called()
    image_remove.assert_not_called()
    container_remove.assert_not_called()


@pytest.mark.parametrize("arch", ["amd64", "x86", "armv5", "armv6", "armv7", "arm64", "ppc64"])
def test_base_build(arch: str, mocker: MockerFixture) -> None:
    """Ensure the base images build correctly."""
    # Mock qemu management
    mocker.patch("etest.build.qemu")

    # Mock build functions
    build = mocker.patch(
        "etest.build.docker.image.build",
        return_value=True,
    )
    run = mocker.patch(
        "etest.build.docker.container.run",
        return_value=True,
    )
    commit = mocker.patch("etest.build.docker.container.commit")

    # Mock cleanup functions
    image_remove = mocker.patch("etest.build.docker.image.remove")
    container_remove = mocker.patch("etest.build.docker.container.remove")

    # Run the program
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--arch", arch, "--verbosity", "DEBUG"])

    # Check for errors
    assert result.exit_code == 0

    # Assert all functions have been called
    build.assert_called_once()
    run.assert_called_once()
    commit.assert_called_once()
    image_remove.assert_called_once()
    container_remove.assert_called_once()


@pytest.mark.parametrize("libc", ["glibc", "musl", "uclibc"])
@pytest.mark.parametrize("hardened", ["--hardened", "--no-hardened"])
def test_alternate_libc_build(libc: str, hardened: str, mocker: MockerFixture) -> None:
    """Ensure images with alternate libcs build correctly."""
    # Mock build functions
    build = mocker.patch(
        "etest.build.docker.image.build",
        return_value=True,
    )
    run = mocker.patch(
        "etest.build.docker.container.run",
        return_value=True,
    )
    commit = mocker.patch("etest.build.docker.container.commit")

    # Mock cleanup functions
    image_remove = mocker.patch("etest.build.docker.image.remove")
    container_remove = mocker.patch("etest.build.docker.container.remove")

    # Run the program
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--libc", libc, hardened, "--verbosity", "DEBUG"])

    # Check for errors
    assert result.exit_code == 0

    # Assert all functions have been called
    build.assert_called_once()
    run.assert_called_once()
    commit.assert_called_once()
    image_remove.assert_called_once()
    container_remove.assert_called_once()


def test_builderror(mocker: MockerFixture) -> None:
    """Ensure the program fails on a BuildError."""
    # Raise a ContainerError
    log = itertools.tee({"error": "mockup"})[0]
    error = docker.errors.BuildError(reason="Mockup error.", build_log=log)

    build = mocker.patch(
        "etest.build.docker.image.build",
        side_effect=error,
    )

    # Run the program
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--verbosity", "DEBUG"])

    # Check if it triggered an error
    assert result.exit_code == 1

    # Assert all functions have been called
    build.assert_called_once()


def test_cleanup(mocker: MockerFixture) -> None:
    """Ensure cleaning happens after exceptions."""
    # Mock build functions
    build = mocker.patch(
        "etest.build.docker.image.build",
        return_value=True,
    )

    # Raise a ContainerError
    error = docker.errors.ContainerError(
        container=True,
        exit_status=1,
        command="ls",
        image="ebuildtest/etest",
        stderr=None,
    )
    run = mocker.patch(
        "etest.build.docker.container.run",
        side_effect=error,
    )

    # Mock cleanup functions
    image_remove = mocker.patch("etest.build.docker.image.remove")
    container_remove = mocker.patch("etest.build.docker.container.remove")

    # Run the program
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--verbosity", "DEBUG"])

    # Check if it triggered an error
    assert result.exit_code == 1

    # Assert all functions have been called
    build.assert_called_once()
    run.assert_called_once()
    image_remove.assert_called_once()
    container_remove.assert_called_once()


def test_push(mocker: MockerFixture) -> None:
    """Ensure etest-build can push."""
    # Mock push functions
    push = mocker.patch(
        "etest.build.docker.image.push",
        return_value="pushing...\nfinished.",
    )

    # Run the program
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--no-build", "--push", "--verbosity", "DEBUG"])

    # Check for errors
    assert result.exit_code == 0

    # Check if logging is handled correctly
    out_debug = [o for o in result.output.splitlines() if "debug" in o]

    assert "debug: pushing..." in out_debug
    assert "debug: finished." in out_debug

    # Check if the program tried pushing
    assert push.asssert_called_once()

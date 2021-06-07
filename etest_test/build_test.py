"""Tests for etest.build."""

import textwrap

import click.testing
import docker
import pytest

import etest.build as sut

# from etest import profile


def test_help() -> None:
    """Ensure etest-build --help exits successfully."""
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--help"])

    assert result.exit_code == 0


def test_nobuild() -> None:
    """Ensure etest-build outputs 3 info lines when not building."""
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--no-build", "--verbosity", "INFO"])

    assert result.exit_code == 0

    out = [o for o in result.output.splitlines() if o]

    assert len(out) == 2


@pytest.mark.slow
def test_amd64_build() -> None:
    """Ensure a base amd64 image builds correctly."""
    runner = click.testing.CliRunner()
    client = docker.APIClient(base_url="unix://var/run/docker.sock")
    result = runner.invoke(sut.main, ["--arch", "amd64", "--verbosity", "DEBUG"])
    output = result.output.lower()

    print(output)

    assert result.exit_code == 0
    assert "error" not in output

    assert "current profile: amd64." in output

    assert "building stage1 image." in output
    assert "debug: stage1 logs:" in output

    assert "building stage2 container." in output
    assert "debug: stage2 logs:" in output

    assert "committing the final image." in output

    assert "cleaning up stage1 image." in output
    assert "cleaning up stage2 container." in output

    assert "etest-build has finished running." in output

    image_data = client.inspect_image("ebuildtest/etest:amd64")

    assert image_data["Architecture"] == "amd64"
    assert image_data["Os"] == "linux"

    assert image_data["ContainerConfig"]["Cmd"] == [
        "/bin/bash",
        "-c",
        textwrap.dedent(sut._libc_commands["glibc"].value)[23:-2],
    ]

    assert image_data["ContainerConfig"]["Image"] == "etest/stage1:amd64"


@pytest.mark.slow
def test_arm64_build() -> None:
    """Ensure a base arm64 image builds correctly."""
    runner = click.testing.CliRunner()
    client = docker.APIClient(base_url="unix://var/run/docker.sock")
    result = runner.invoke(sut.main, ["--arch", "arm64"])

    assert result.exit_code == 0

    image_data = client.inspect_image("ebuildtest/etest:arm64")

    assert image_data["Architecture"] == "arm64"
    assert image_data["Os"] == "linux"

    print(image_data["ContainerConfig"]["Cmd"])
    print(
        [
            "/bin/bash",
            "-c",
            textwrap.dedent(sut._libc_commands["glibc"].value)[23:-2],
        ],
    )

    assert image_data["ContainerConfig"]["Cmd"] == [
        "/bin/bash",
        "-c",
        textwrap.dedent(sut._libc_commands["glibc"].value)[23:-2],
    ]

    assert image_data["ContainerConfig"]["Image"] == "etest/stage1:arm64"


@pytest.mark.slow
def test_musl_build() -> None:
    """Ensure a base musl image builds correctly."""
    runner = click.testing.CliRunner()
    client = docker.APIClient(base_url="unix://var/run/docker.sock")
    result = runner.invoke(sut.main, ["--arch", "amd64", "--libc", "musl"])

    assert result.exit_code == 0

    image_data = client.inspect_image("ebuildtest/etest:amd64-musl-vanilla")

    assert image_data["Architecture"] == "amd64"
    assert image_data["Os"] == "linux"

    assert image_data["ContainerConfig"]["Cmd"] == [
        "/bin/bash",
        "-c",
        textwrap.dedent(sut._libc_commands["musl"].value)[23:-2],
    ]

    assert image_data["ContainerConfig"]["Image"] == "etest/stage1:amd64-musl-vanilla"


@pytest.mark.slow
def test_uclibc_build() -> None:
    """Ensure a base uclibc image builds correctly."""
    runner = click.testing.CliRunner()
    client = docker.APIClient(base_url="unix://var/run/docker.sock")
    result = runner.invoke(sut.main, ["--arch", "amd64", "--libc", "uclibc"])

    assert result.exit_code == 0

    image_data = client.inspect_image("ebuildtest/etest:amd64-uclibc-vanilla")

    assert image_data["Architecture"] == "amd64"
    assert image_data["Os"] == "linux"

    assert image_data["ContainerConfig"]["Cmd"] == [
        "/bin/bash",
        "-c",
        textwrap.dedent(sut._libc_commands["uclibc"].value)[13:],
    ]

    assert image_data["ContainerConfig"]["Image"] == "etest/stage1:amd64-uclibc-vanilla"


# @pytest.mark.skip("Invalid. Rewrite")
# def test_image_cleanup(capfd: pytest.CaptureFixture[str]) -> None:
# """Ensure the stage1 image is cleaned."""
# profile_ = profile.Profile(False, "amd64", "glibc", False, True, False)
# profile_.profile = profile_.docker = "twitter"  # Garbage in

# client = docker.from_env()

# try:
# sut._build_image(profile_, ".")
# except docker.errors.BuildError:
# pass

# image = None
# try:
# image = client.images.get(f"etest/stage1:{profile_.profile}")
# except docker.errors.NotFound:
# pass

# assert image is None

# captured = capfd.readouterr()
# error = [e for e in captured.err.splitlines() if "error: " in e]

# assert len(error) > 3


# @pytest.mark.skip("Invalid. Rewrite")
# def test_container_cleanup(capfd: pytest.CaptureFixture[str]) -> None:
# """Ensure the stage2 container is cleaned."""
# profile_ = profile.Profile(False, "amd64", "uclibc", False, True, False)
# profile_.libc = "glibc"  # Garbage in

# client = docker.from_env()

# try:
# sut._build_image(profile_, ".")
# except docker.errors.ContainerError:
# pass

# container = None
# try:
# container = client.containers.get(f"stage2-{profile_.profile}")
# except docker.errors.NotFound:
# pass

# assert container is None

# captured = capfd.readouterr()
# error = [e for e in captured.err.splitlines() if "error: " in e]

# assert len(error) > 2


@pytest.mark.slow
def test_push() -> None:
    """Ensure etest-build can push."""
    runner = click.testing.CliRunner()
    result = runner.invoke(sut.main, ["--no-build", "--push", "--verbosity", "DEBUG"])

    assert result.exit_code == 0

    out = [o for o in result.output.splitlines() if "debug" not in o]
    out_debug = [o for o in result.output.splitlines() if "debug" in o]

    assert len(out) == 4
    assert "error" not in out_debug

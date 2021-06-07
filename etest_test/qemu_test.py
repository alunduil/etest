"""Tests for etest.qemu."""

import logging

import docker
import pytest
from pytest_mock import MockerFixture

import etest.qemu as sut


@pytest.mark.parametrize("arch", ["x86", "armv5", "armv6", "armv7", "arm64", "ppc64"])
def test_non_amd64(arch: str, mocker: MockerFixture) -> None:
    """Ensure QEMU starts on different architectures."""
    # Mock the docker API
    pull = mocker.patch("etest.qemu.docker.pull")
    create = mocker.patch(
        "etest.qemu.docker.container.create",
        return_value=True,
    )
    start = mocker.patch("etest.qemu.docker.container.start")
    remove = mocker.patch(
        "etest.qemu.docker.container.remove",
        return_value=True,
    )

    # Start QEMU
    qemu = sut.qemu(arch)
    qemu.__enter__()
    assert qemu.enabled
    qemu.__exit__()

    # Assert all the functions have been called
    pull.assert_called_once()
    create.assert_called_once()
    start.assert_called_once()
    remove.assert_called_once()


@pytest.mark.slow
def test_qemu_integration(caplog: pytest.LogCaptureFixture) -> None:
    """Ensure QEMU is working."""
    client = docker.from_env()
    image = "arm64v8/alpine"

    caplog.set_level(logging.DEBUG)

    client.images.pull(image)

    with sut.qemu("arm64"):
        assert client.containers.run(image, "uname -m", remove=True, tty=True) == b"aarch64\r\n"
        assert caplog.text
        caplog.clear()

    assert caplog.text
    caplog.clear()


def test_enter_skip_on_amd64(caplog: pytest.LogCaptureFixture) -> None:
    """Ensure __enter__ skips execution when it's innecessary."""
    caplog.set_level(logging.DEBUG)
    qemu = sut.qemu("amd64")

    qemu.__enter__()
    log = caplog.text
    caplog.clear()

    assert not log


def test_exit_skip_on_amd64(caplog: pytest.LogCaptureFixture) -> None:
    """Ensure __exit__ skips execution when it's innecessary."""
    caplog.set_level(logging.DEBUG)
    qemu = sut.qemu("amd64")

    qemu.__exit__()
    log = caplog.text
    caplog.clear()

    assert not log

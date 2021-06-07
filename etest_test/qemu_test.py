"""Tests for etest.qemu."""

import logging

import docker
import pytest

import etest.qemu as sut


def test_non_amd64() -> None:
    """Ensure QEMU only opens on non-amd64 architectures."""
    assert sut.qemu("amd64").enabled is False

    for arch in ["x86", "armv5", "armv6", "armv7", "arm64", "ppc64"]:
        assert sut.qemu(arch).enabled


@pytest.mark.slow
def test_qemu_works(caplog: pytest.LogCaptureFixture) -> None:
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

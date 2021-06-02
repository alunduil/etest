"""Tests for etest.qemu."""

import logging
from typing import Any

import docker
import pytest

import etest.qemu as sut

logger = logging.getLogger(__name__)


def test_init() -> None:
    """Ensure QEMU only opens on non-amd64 architectures."""
    assert sut.qemu(logger, "amd64").get_enabled() is False

    for arch in ["x86", "armv5", "armv6", "armv7", "arm64", "ppc64"]:
        assert sut.qemu(logger, arch).get_enabled()


@pytest.mark.slow
def test_qemu_works(caplog: Any) -> None:
    """Ensure QEMU is working."""
    client = docker.from_env()
    image = "arm64v8/alpine"

    caplog.set_level(logging.DEBUG)

    client.images.pull(image)

    with sut.qemu(logger, "arm64"):
        assert client.containers.run(image, "uname -m", remove=True, tty=True) == b"aarch64\r\n"
        assert caplog.text
        caplog.clear()

    assert caplog.text
    caplog.clear()


def test_function_pass(caplog: Any) -> None:
    """Ensure __enter__ and __exit__ skip execution when necessary."""
    qemu = sut.qemu(logger, "amd64")
    caplog.set_level(logging.DEBUG)

    qemu.__enter__()
    log = caplog.text
    caplog.clear()

    assert not log

    qemu.__exit__()
    log = caplog.text
    caplog.clear()

    assert not log

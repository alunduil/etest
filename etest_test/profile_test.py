"""Tests for etest.profile."""

import logging
from typing import Any

import etest.profile as sut

logger = logging.getLogger(__name__)


def test_base_arch() -> None:
    """Ensure base arches work."""
    for arch in ["amd64", "x86", "arm64"]:
        result = sut.Profile(False, arch, "glibc", False, True, False)

        # Check profile strings
        assert result.profile == arch
        assert result.docker == arch

        # Check arch values
        assert result.arch == arch
        assert result.pkg_arch == arch
        assert result.docker_arch == arch

        # Check profile options
        assert result.hardened is False
        assert result.multilib is True
        assert result.systemd is False

        # Check libc
        assert result.libc == "glibc"


def test_base_ppc64() -> None:
    """Ensure the ppc64 base arch works."""
    arch = "ppc64"
    docker_arch = "ppc64le"

    result = sut.Profile(False, arch, "glibc", False, True, False)

    # Check profile strings
    assert result.profile == arch
    assert result.docker == docker_arch

    # Check arch values
    assert result.arch == arch
    assert result.pkg_arch == "ppc64"
    assert result.docker_arch == docker_arch

    # Check profile options
    assert result.hardened is False
    assert result.multilib is True
    assert result.systemd is False

    # Check libc
    assert result.libc == "glibc"


def test_base_arm() -> None:
    """Ensure ARM base arches work."""
    docker_arm_mappings = {"armv5": "armv5tel", "armv6": "armv6j_hardfp", "armv7": "armv7a_hardfp"}

    for arch in ["armv5", "armv6", "armv7"]:
        result = sut.Profile(False, arch, "glibc", False, True, False)

        # Check profile strings
        assert result.profile == arch
        assert result.docker == docker_arm_mappings[arch]

        # Check arch values
        assert result.arch == arch
        assert result.pkg_arch == "arm"
        assert result.docker_arch == docker_arm_mappings[arch]

        # Check profile options
        assert result.hardened is False
        assert result.multilib is True
        assert result.systemd is False

        # Check libc
        assert result.libc == "glibc"


def test_libc() -> None:
    """Ensure alternative libcs work."""
    arch = "amd64"

    for libc in ["musl", "uclibc"]:
        result_vanilla = sut.Profile(False, arch, libc, False, True, False)
        result_hardened = sut.Profile(False, arch, libc, True, True, False)

        # Check profile strings
        assert result_vanilla.profile == f"{arch}-{libc}-vanilla"
        assert result_vanilla.docker == f"{arch}-{libc}-vanilla"
        assert result_hardened.profile == f"{arch}-{libc}-hardened"
        assert result_hardened.docker == f"{arch}-{libc}-hardened"

        # Check arch values
        assert result_vanilla.arch == result_hardened.arch == arch
        assert result_vanilla.pkg_arch == result_hardened.pkg_arch == arch
        assert result_vanilla.docker_arch == result_hardened.docker_arch == arch

        # Check profile options
        assert result_vanilla.hardened is False
        assert result_hardened.hardened is True
        assert result_vanilla.multilib is True
        assert result_hardened.multilib is True
        assert result_vanilla.systemd is False
        assert result_hardened.systemd is False

        # Check libc
        assert result_vanilla.libc == result_hardened.libc == libc


def try_invalid_profile(*args: Any, **kwargs: Any) -> bool:
    """Try an invalid profile."""
    e = False

    try:
        sut.Profile(*args, **kwargs)
    except sut.InvalidProfileError:
        e = True

    return e


def test_invalid_arm_profiles() -> None:
    """Ensure invalid ARM profiles raise exceptions."""
    for arch in ["armv5", "armv6", "armv7"]:
        # Alternative libcs
        for libc in ["musl", "uclibc"]:
            assert try_invalid_profile(False, arch, libc, False, True, False)

        # Hardened
        assert try_invalid_profile(False, arch, "glibc", True, True, False)

        # Systemd
        assert try_invalid_profile(False, arch, "glibc", False, True, True)


def test_invalid_arm64_profiles() -> None:
    """Ensure invalid ARM profiles raise exceptions."""
    arch = "arm64"

    # Alternative libcs
    for libc in ["musl", "uclibc"]:
        assert try_invalid_profile(False, arch, libc, False, True, False)

    # Hardened
    assert try_invalid_profile(False, arch, "glibc", True, True, False)


def test_invalid_x86_profiles() -> None:
    """Ensure invalid x86 profiles raise exceptions."""
    arch = "x86"

    # Hardened musl
    assert try_invalid_profile(False, arch, "musl", True, True, False)


def test_invalid_ppc64_profiles() -> None:
    """Ensure invalid ppc64 profiles raise exceptions."""
    arch = "ppc64"

    # uclibc
    assert try_invalid_profile(False, arch, "uclibc", False, True, False)

    # Vanilla musl
    assert try_invalid_profile(False, arch, "musl", False, True, False)

    # Hardened
    assert try_invalid_profile(False, arch, "glibc", True, True, False)


def test_systemd() -> None:
    """Ensure systemd profiles work correctly."""
    for arch in ["amd64", "x86", "arm64", "ppc64"]:
        # Base
        result = sut.Profile(False, arch, "glibc", False, True, True)
        assert result.profile == f"{arch}-systemd"

        # Alternative libcs
        for libc in ["musl", "uclibc"]:
            assert try_invalid_profile(False, arch, libc, False, True, True)

        # Hardened
        assert try_invalid_profile(False, arch, "glibc", True, True, True)

    # No multilib
    assert try_invalid_profile(False, "amd64", "glibc", False, False, True)


def test_no_multilib() -> None:
    """Ensure no-multilib only affects AMD64."""
    # Other arches
    for arch in ["x86", "armv5", "armv6", "armv7", "arm64", "ppc64"]:
        assert try_invalid_profile(True, arch, "glibc", False, False, False)

    arch = "amd64"

    # Base
    result = sut.Profile(False, arch, "glibc", False, False, False)
    assert result.profile == f"{arch}-nomultilib"

    # Hardened
    result = sut.Profile(False, arch, "glibc", True, False, False)
    assert result.profile == f"{arch}-hardened-nomultilib"

    # Alternative libcs
    for libc in ["musl", "uclibc"]:
        assert try_invalid_profile(False, arch, libc, False, False, False)

    # Systemd
    assert try_invalid_profile(False, arch, "glibc", False, False, True)


def test_warnings() -> None:
    """Ensure warnings happen correctly."""
    # No multilib warning
    assert try_invalid_profile(False, "armv7", "glibc", False, False, False) is False
    assert try_invalid_profile(True, "armv7", "glibc", False, False, False)

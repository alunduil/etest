"""Tests for etest.profile."""

import logging
from typing import Any, Dict

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from pytest_mock import MockerFixture

import etest.profile as sut

logger = logging.getLogger(__name__)


_valid_architectures = ["amd64", "x86", "armv5", "armv6", "armv7", "arm64", "ppc64"]
_valid_systemd_architectures = ["amd64", "x86", "arm64", "ppc64"]
_libc_value = ["glibc", "musl", "uclibc"]


@st.composite
def non_base_profiles(draw: Any) -> Dict[str, Any]:
    """Strategy for generating non-base profiles."""
    # Draw values
    profile = {}
    profile["libc"] = draw(st.sampled_from(_libc_value))
    profile["hardened"] = draw(st.booleans())
    profile["multilib"] = draw(st.booleans())
    profile["systemd"] = draw(st.booleans())

    # Ensure it isn't a base profile
    assume(profile != {"libc": "glibc", "hardened": False, "multilib": True, "systemd": False})

    return profile


@pytest.mark.parametrize("arch", _valid_architectures)
def test_base_arch(arch: str) -> None:
    """Ensure the base profiles work."""
    result = sut.Profile(False, arch, "glibc", False, True, False)

    # Check profile strings
    assert result.profile == arch


@pytest.mark.parametrize("libc", ["musl", "uclibc"])
@pytest.mark.parametrize("hardened", [True, False])
def test_amd64_libc(libc: str, hardened: bool) -> None:
    """Ensure alternative libcs work on amd64."""
    arch = "amd64"

    result = sut.Profile(True, arch, libc, hardened, True, False)

    # Check the profile string
    result_suffix = "hardened" if hardened else "vanilla"
    assert result.profile == f"{arch}-{libc}-{result_suffix}"


@pytest.mark.parametrize("arch", ["armv5", "armv6", "armv7"])
@given(profile=non_base_profiles())
def test_invalid_arm_profiles(arch: str, profile: Dict[str, Any]) -> None:
    """Ensure non-base ARM profiles raise exceptions."""
    with pytest.raises(sut.InvalidProfileError):
        sut.Profile(True, arch, profile["libc"], profile["hardened"], profile["multilib"], profile["systemd"])


@given(profile=non_base_profiles())
def test_invalid_arm64_profiles(profile: Dict[str, Any]) -> None:
    """Ensure invalid ARM64 profiles raise exceptions."""
    arch = "arm64"

    # Dont test arm64-systemd, as it is a valid profile
    assume(profile != {"libc": "glibc", "hardened": False, "multilib": True, "systemd": True})

    with pytest.raises(sut.InvalidProfileError):
        sut.Profile(True, arch, profile["libc"], profile["hardened"], profile["multilib"], profile["systemd"])


@given(profile=non_base_profiles())
def test_invalid_x86_profiles(profile: Dict[str, Any]) -> None:
    """Ensure invalid x86 profiles raise exceptions."""
    arch = "x86"

    # Dont test: x86-hardened, x86-musl-vanilla, x86-systemd, x86-uclibc-vanilla, x86-uclibc-hardened
    assume(profile != {"libc": "glibc", "hardened": True, "multilib": True, "systemd": False})
    assume(profile != {"libc": "musl", "hardened": False, "multilib": True, "systemd": False})
    assume(profile != {"libc": "glibc", "hardened": False, "multilib": True, "systemd": True})
    assume(profile != {"libc": "uclibc", "hardened": False, "multilib": True, "systemd": False})
    assume(profile != {"libc": "uclibc", "hardened": True, "multilib": True, "systemd": False})

    with pytest.raises(sut.InvalidProfileError):
        sut.Profile(True, arch, profile["libc"], profile["hardened"], profile["multilib"], profile["systemd"])


@given(profile=non_base_profiles())
def test_invalid_ppc64_profiles(profile: Dict[str, Any]) -> None:
    """Ensure invalid ppc64 profiles raise exceptions."""
    arch = "ppc64"

    # Dont test ppc64-systemd or ppc64-musl-vanilla
    assume(profile != {"libc": "glibc", "hardened": False, "multilib": True, "systemd": True})
    assume(profile != {"libc": "musl", "hardened": True, "multilib": True, "systemd": False})

    with pytest.raises(sut.InvalidProfileError):
        sut.Profile(True, arch, profile["libc"], profile["hardened"], profile["multilib"], profile["systemd"])


@pytest.mark.parametrize("arch", _valid_systemd_architectures)
def test_systemd(arch: str) -> None:
    """Ensure systemd profiles work correctly."""
    result = sut.Profile(False, arch, "glibc", False, True, True)
    assert result.profile == f"{arch}-systemd"


@pytest.mark.parametrize("arch", _valid_systemd_architectures)
@given(profile=non_base_profiles())
def test_invalid_systemd(arch: str, profile: Dict[str, Any]) -> None:
    """Ensure invalid systemd profiles raise exceptions."""
    # We could generate valid systemd profiles, so remove every profile with systemd enabled
    assume(profile["systemd"] is False)

    # Ensure it raises an InvalidProfileError
    with pytest.raises(sut.InvalidProfileError):
        sut.Profile(True, arch, profile["libc"], profile["hardened"], profile["multilib"], True)


@pytest.mark.parametrize("arch", [a for a in _valid_architectures if a != "amd64"])
def test_no_multilib_warnings(arch: str, mocker: MockerFixture) -> None:
    """Ensure warnings happen when using no-multilib outside amd64."""
    # Peek into usage of the logging functions
    warning = mocker.spy(sut._LOGGER, "warning")
    error = mocker.spy(sut._LOGGER, "error")

    # Check for warnings when not using --strict
    sut.Profile(False, arch, "glibc", False, False, False)
    warning.assert_called_once()

    # Check for errors when using --strict
    with pytest.raises(sut.InvalidProfileError):
        sut.Profile(True, arch, "glibc", False, False, False)
    error.assert_called_once()


@pytest.mark.parametrize("hardened", [True, False])
def test_no_multilib_amd64(hardened: bool) -> None:
    """Ensure no-multilib works on amd64."""
    arch = "amd64"

    result = sut.Profile(True, arch, "glibc", hardened, False, False)

    # Check the profile string
    hardened_ = "-hardened" if hardened else ""
    assert result.profile == f"{arch}{hardened_}-nomultilib"

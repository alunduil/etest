"""Profile definitions and builders."""

import functools
import logging
from enum import Enum

_LOGGER = logging.getLogger()


class _ARMIdentifier(Enum):
    armv5 = "armv5tel"
    armv6 = "armv6j_hardfp"
    armv7 = "armv7a_hardfp"
    arm64 = "arm64"


class InvalidProfileError(ValueError):
    """The profile is invalid."""

    pass


class Profile:
    """A class to generate profile options."""

    def __init__(
        self,
        strict: bool,
        arch: str,
        libc: str,
        hardened: bool,
        multilib: bool,
        systemd: bool,
    ) -> None:
        """Initialize parameters."""
        self._strict = strict

        self._arch = arch
        self._docker_arch = arch
        self._pkg_arch = arch

        self._libc = libc
        self._hardened = hardened

        self._multilib = multilib

        self._systemd = systemd

        _LOGGER.info("Standarizing profile data.")
        self._standarize()

    @property
    def strict(self) -> bool:
        """Error on warnings."""
        return self._strict

    @property
    def arch(self) -> str:
        """Architecture to use."""
        return self._arch

    @property
    def docker_arch(self) -> str:
        """Architecture for the docker base image."""
        return self._docker_arch

    @docker_arch.setter
    def docker_arch(self, value: str) -> None:
        self._docker_arch = value

    @property
    def pkg_arch(self) -> str:
        """Gentoo package architecture."""
        return self._pkg_arch

    @pkg_arch.setter
    def pkg_arch(self, value: str) -> None:
        self._pkg_arch = value

    @property
    def libc(self) -> str:
        """Libc to be used."""
        return self._libc

    @property
    def hardened(self) -> bool:
        """Use hardening."""
        return self._hardened

    @property
    def multilib(self) -> bool:
        """Use multilib."""
        return self._multilib

    @multilib.setter
    def multilib(self, value: bool) -> None:
        self._multilib = value

    @property
    def systemd(self) -> bool:
        """Use systemd."""
        return self._systemd

    @functools.cached_property
    def base_profile(self) -> str:
        """Build profile information."""
        base_profile = ""

        if self.libc != "glibc":
            base_profile += f"-{self.libc}"

        if self.hardened:
            base_profile += "-hardened"
        elif self.libc != "glibc":
            base_profile += "-vanilla"

        if not self.multilib:
            base_profile += "-nomultilib"

        if self.systemd:
            base_profile += "-systemd"

        return base_profile

    @property
    def profile(self) -> str:
        """Profile to use."""
        return self.arch + self.base_profile

    @property
    def docker_profile(self) -> str:
        """Profile to use for the base image."""
        return self.docker_arch + self.base_profile

    def _warn(self, message: str) -> None:
        """Give a warning to the user."""
        if not self.strict:
            _LOGGER.warning(message)
        else:
            self._error(message)

    def _error(self, message: str) -> None:
        """Raise an error."""
        _LOGGER.error(message)
        raise InvalidProfileError(message)

    def _standarize(self) -> None:
        """Sanitize profile settings."""
        if "arm" in self.arch:
            self.docker_arch = _ARMIdentifier[self.arch].value

            if "armv" in self.arch:
                self.pkg_arch = "arm"

            if self.hardened or self.libc != "glibc":
                self._error("The ARM architecture can't use a different libc or hardened profiles.")
            if self.systemd and self.arch != "arm64":
                self._error(f"{self.arch} doesn't support systemd.")

        if self.arch == "ppc64":
            self.docker_arch = "ppc64le"

            if self.libc == "uclibc":
                self._error("The PPC64 architecture doesn't support uclibc.")
            if self.libc == "musl" and not self.hardened:
                self._error("The PPC64 architecture doesn't support vanilla musl.")
            if self.libc == "glibc" and self.hardened:
                self._error("The PPC64 architecture doesn't support hardened glibc.")

        if self.arch == "x86":
            if self.libc == "musl" and self.hardened:
                self._error("The x86 architecture doesn't support hardened musl.")

        if self.arch != "amd64" and not self.multilib:
            self.multilib = True
            self._warn("--no-multilib is specific to AMD64.")

        if self.libc != "glibc" and not self.multilib:
            self._error("Alternative libcs dont support no-multilib.")

        if self.systemd and (self.hardened or not self.multilib or self.libc != "glibc"):
            self._error("Systemd profiles doesn't support alternative libcs, hardening or no multilib.")

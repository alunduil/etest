"""Profile definitions and builders."""

import logging
from enum import Enum


class _arm_mappings(Enum):
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
        logger: logging.Logger,
        strict: bool,
        arch: str,
        libc: str,
        hardened: bool,
        multilib: bool,
        systemd: bool,
    ) -> None:
        """Initialize parameters."""
        self.logger = logger
        self.strict = strict

        self.arch = arch
        self.docker_arch = arch
        self.pkg_arch = arch

        self.libc = libc
        self.hardened = hardened

        self.multilib = multilib

        self.systemd = systemd

        self.logger.info("Standarizing profile data.")
        self._standarize()
        self.logger.info("Building profile strings.")
        self._build()

    def _warn(self, message: str) -> None:
        """Give a warning to the user."""
        if not self.strict:
            self.logger.warning(message)
        else:
            self._error(message)

    def _error(self, message: str) -> None:
        """Raise an error."""
        self.logger.error(message)
        raise InvalidProfileError(message)

    def _standarize(self) -> None:
        """Sanitize profile settings."""
        if "arm" in self.arch:
            self.docker_arch = _arm_mappings[self.arch].value

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

    def _build(self) -> None:
        """Build profile information."""
        self.profile = ""

        if self.libc != "glibc":
            self.profile += f"-{self.libc}"

        if self.hardened:
            self.profile += "-hardened"
        elif self.libc != "glibc":
            self.profile += "-vanilla"

        if not self.multilib:
            self.profile += "-nomultilib"

        if self.systemd:
            self.profile += "-systemd"

        self.docker = self.docker_arch + self.profile
        self.profile = self.arch + self.profile

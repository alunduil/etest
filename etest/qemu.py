"""QEMU interpreter management."""

# Please see https://github.com/multiarch/qemu-user-static

import logging
from typing import Any

from etest import docker

_LOGGER = logging.getLogger()


class qemu:
    """QEMU interpreter management."""

    def __init__(self, arch: str) -> None:
        """Initialize."""
        self._arch = arch

    @property
    def arch(self) -> str:
        """Architecture being used."""
        return self._arch

    @property
    def enabled(self) -> bool:
        """Check if QEMU should be enabled."""
        return self.arch != "amd64"

    def __enter__(self) -> None:
        """Start the QEMU interpreter."""
        if self.enabled:
            _LOGGER.info("Enabling QEMU.")

            _LOGGER.debug("Pulling QEMU image.")
            docker.pull("multiarch/qemu-user-static:latest")

            _LOGGER.debug("Creating QEMU container.")
            self.container = docker.container.create(
                image="multiarch/qemu-user-static",
                privileged=True,
                command="--reset -p yes",
            )

            docker.container.start(self.container)

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Kill the QEMU interpreter."""
        if self.enabled:
            _LOGGER.info("Exiting QEMU.")
            docker.container.remove(self.container)

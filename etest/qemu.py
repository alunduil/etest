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
        if arch != "amd64":
            self.__enabled = True
        else:
            self.__enabled = False

    def __enter__(self) -> None:
        """Start the QEMU interpreter."""
        if self.__enabled:
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
        if self.__enabled:
            _LOGGER.info("Exiting QEMU.")
            docker.container.remove(self.container)

    def get_enabled(self) -> bool:
        """Check if QEMU is enabled."""
        return self.__enabled

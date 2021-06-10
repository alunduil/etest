"""QEMU interpreter management."""

# Please see https://github.com/multiarch/qemu-user-static

import logging
from typing import Any

from etest import docker


class qemu:
    """QEMU interpreter management."""

    def __init__(self, logger: logging.Logger, arch: str) -> None:
        """Initialize."""
        self.logger = logger

        if arch != "amd64":
            self.__enabled = True
        else:
            self.__enabled = False

    def __enter__(self) -> None:
        """Start the QEMU interpreter."""
        if self.__enabled:
            self.logger.info("Enabling QEMU.")

            self.logger.debug("Pulling QEMU image.")
            docker.pull("multiarch/qemu-user-static:latest")

            self.logger.debug("Creating QEMU container.")
            self.container = docker.container.create(
                image="multiarch/qemu-user-static",
                privileged=True,
                command="--reset -p yes",
            )

            docker.container.start(self.container)

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        """Kill the QEMU interpreter."""
        if self.__enabled:
            self.logger.info("Exiting QEMU.")
            docker.container.remove(self.container)

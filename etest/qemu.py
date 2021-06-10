"""QEMU interpreter management."""

# Please see https://github.com/multiarch/qemu-user-static

from typing import Any

from etest import docker


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
            docker.pull("multiarch/qemu-user-static:latest")

            self.container = docker.container.create(
                image="multiarch/qemu-user-static",
                privileged=True,
                command="--reset -p yes",
            )

            docker.container.start(self.container)

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        """Kill the QEMU interpreter."""
        if self.__enabled:
            docker.container.remove(self.container)

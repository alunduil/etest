"""QEMU interpreter management."""

# Please see https://github.com/multiarch/qemu-user-static

from etest import docker


class qemu:
    """QEMU interpreter management."""

    def __init__(self, arch: str):
        """Initialize."""
        if arch != "amd64":
            self.__enabled = True
        else:
            self.__enabled = False

    def __enter__(self):
        """Start the QEMU interpreter."""
        if self.__enabled:
            docker.pull("multiarch/qemu-user-static:latest")

            self.container = docker.container.create_simple(
                image="multiarch/qemu-user-static",
                privileged=True,
                command="--reset -p yes",
            )

            docker.container.start(self.container)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Kill the QEMU interpreter."""
        if self.__enabled:
            docker.container.remove(self.container)

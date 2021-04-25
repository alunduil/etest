"""QEMU interpreter management."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from etest import docker


class qemu:
    """QEMU interpreter management."""

    def __init__(self, arch: str):
        """Initialize."""
        if arch != "amd64":
            self.enabled = True

    def __enter__(self):
        """Start the QEMU interpreter."""
        if self.enabled:
            docker.pull("multiarch/qemu-user-static:latest")

            self.container = docker.container.create_simple(
                image="multiarch/qemu-user-static",
                privileged=True,
                command="--reset -p yes",
            )

            docker.container.start(self.container)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Kill the QEMU interpreter."""
        if self.enabled:
            docker.container.remove(self.container)

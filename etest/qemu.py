"""QEMU interpreter management."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from etest import docker


def start():
    """Start the QEMU interpreter."""
    docker.pull("multiarch/qemu-user-static")

    global QEMU_CONTAINER

    QEMU_CONTAINER = docker.container.create(
        autoconf=False,
        image="multiarch/qemu-user-static",
        privileged=True,
        command="--reset -p yes",
    )

    docker.container.start(QEMU_CONTAINER)


def exit():
    """Kill the QEMU interpreter."""
    docker.container.remove(QEMU_CONTAINER)

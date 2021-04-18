"""Docker container."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from typing import List

from etest.docker import common

CONTAINERS: List = []
CREATE = True


def commit(*args, **kwargs):
    """Commit a Docker container."""
    return common.CLIENT.commit(*args, **kwargs)


def create(*args, **kwargs):
    """Create a Docker container."""
    container = common.CLIENT.containers.create(*args, **kwargs)

    CONTAINERS.append(container)
    return container


def logs(*args, **kwargs):
    """Show logs of a Docker container."""
    return common.API_CLIENT.logs(*args, **kwargs)


def remove(container, container_name, *args, **kwargs):
    """Remove a Docker container."""
    CONTAINERS.remove(container)
    return common.API_CLIENT.remove_container(container_name, *args, **kwargs)


def start(container, *args, **kwargs):
    """Start a Docker container."""
    if not CREATE:
        return False

    container.start()

    return True


def stop(container, *args, **kwargs):
    """Stop a Docker container."""
    return common.API_CLIENT.stop(container, *args, **kwargs)


def wait(*args, **kwargs):
    """Wait for Docker container."""
    return common.API_CLIENT.wait(*args, **kwargs)

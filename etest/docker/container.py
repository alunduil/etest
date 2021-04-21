"""Docker container."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from typing import List

from etest.docker import common

CONTAINERS: List = []
CREATE = True


def commit(container, *args, **kwargs):
    """Commit a Docker container."""
    return container.commit(*args, **kwargs)


def create(overlay: str, *args, **kwargs):
    """Create a Docker container."""
    container_data = common.API_CLIENT.create_container(
        *args,
        **kwargs,
        host_config=common.API_CLIENT.create_host_config(
            binds={
                overlay: {
                    "bind": "/overlay",
                    "ro": True,
                },
                # TODO: Retrieve this from environment.
                "/usr/portage": {
                    "bind": "/usr/portage",
                    "ro": True,
                },
            },
        )
    )

    print(container_data)
    container = common.CLIENT.containers.get(container_data["Id"])

    CONTAINERS.append(container)
    return container


def logs(*args, **kwargs):
    """Show logs of a Docker container."""
    return common.API_CLIENT.logs(*args, **kwargs)


def remove(container, container_name, *args, **kwargs):
    """Remove a Docker container."""
    CONTAINERS.remove(container)
    return common.API_CLIENT.remove_container(container_name, *args, **kwargs)


def start(container):
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

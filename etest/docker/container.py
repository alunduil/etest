"""Docker container."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from typing import List

from docker.models.containers import Container

from etest.docker import common

CONTAINERS: List = []
CREATE = True


def commit(container: Container, tag: str, repository: str, *args, **kwargs):
    """Commit a Docker container."""
    print(repository)
    repo = repository.replace("=", "").replace("[", "").replace("]", "").replace(",", "")

    container.commit(repository=repo, tag=tag, *args, **kwargs)

    return repo + ":" + tag


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

    container = common.CLIENT.containers.get(container_data["Id"])

    CONTAINERS.append(container)
    return container


def logs(*args, **kwargs):
    """Show logs of a Docker container."""
    return common.API_CLIENT.logs(*args, **kwargs)


def remove(container: Container, *args, **kwargs):
    """Remove a Docker container."""
    CONTAINERS.remove(container)
    return container.remove(**kwargs)


def start(container: Container):
    """Start a Docker container."""
    if not CREATE:
        return False

    container.start()

    return True


def stop(container: Container, *args, **kwargs):
    """Stop a Docker container."""
    return common.API_CLIENT.stop(container, *args, **kwargs)


def wait(*args, **kwargs):
    """Wait for Docker container."""
    return common.API_CLIENT.wait(*args, **kwargs)

"""Docker container."""

import logging
from pathlib import Path
from typing import Any, List, Optional

from docker.models.containers import Container

from etest.docker import common

CONTAINERS: List[Container] = []
CREATE = True

_LOGGER = logging.getLogger()


def commit(container: Container, tag: str, repository: str, *args: Any, **kwargs: Any) -> str:
    """Commit a Docker container."""
    repo = "".join([c for c in repository if c not in "=[],"]).lower()

    container.commit(repository=repo, tag=tag, *args, **kwargs)

    return repo + ":" + tag


def create(overlay: Optional[Path] = None, *args: Any, **kwargs: Any) -> Container:
    """Create a docker container."""
    if overlay:
        return _create_low_level(overlay, *args, **kwargs)
    else:
        return _create_high_level(*args, **kwargs)


def _create_low_level(overlay: Path, *args, **kwargs):
    """Create a Docker container via the low-level API."""
    container_data = common.API_CLIENT.create_container(
        *args,
        **kwargs,
        host_config=common.API_CLIENT.create_host_config(
            binds={
                str(overlay): {
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


def _create_high_level(*args, **kwargs):
    """Create a Docker container via the high-level API."""
    container = common.CLIENT.containers.create(*args, **kwargs)

    CONTAINERS.append(container)
    return container


def logs(*args: Any, **kwargs: Any) -> Any:
    """Show logs of a Docker container."""
    return common.API_CLIENT.logs(*args, **kwargs)


def remove(container: Container, *args: Any, **kwargs: Any) -> Any:
    """Remove a Docker container."""
    if container in CONTAINERS:
        CONTAINERS.remove(container)

    return container.remove(**kwargs)


def start(container: Container) -> bool:
    """Start a Docker container."""
    if not CREATE:
        return False

    container.start()

    return True


def stop(container: Container, *args: Any, **kwargs: Any) -> Any:
    """Stop a Docker container."""
    return common.API_CLIENT.stop(container, *args, **kwargs)


def wait(*args: Any, **kwargs: Any) -> Any:
    """Wait for Docker container."""
    return common.API_CLIENT.wait(*args, **kwargs)


def run(name: str, *args: Any, **kwargs: Any) -> Container:
    """Run a Docker container."""
    logs = common.CLIENT.containers.run(name=name, **kwargs)
    container = common.CLIENT.containers.get(name)
    CONTAINERS.append(container)

    for line in logs.split(b"\n"):
        if line:
            _LOGGER.debug(line.decode())

    return container

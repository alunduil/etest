"""Docker container."""
from typing import Any, List

from docker.models.containers import Container

from etest.docker import common

CONTAINERS: List[Container] = []
CREATE = True


def commit(container: Container, tag: str, repository: str, *args: Any, **kwargs: Any) -> str:
    """Commit a Docker container."""
    repo = "".join([c for c in repository if c not in "=[],"]).lower()

    container.commit(repository=repo, tag=tag, *args, **kwargs)
    
    return repo + ":" + tag


def create(overlay: str, *args: Any, **kwargs: Any) -> Container:
    """Create a docker container."""
    if overlay:
        return create_low_level(overlay, *args, **kwargs)
    else:
        return create_high_level(*args, **kwargs)


def create_low_level(overlay: str, *args, **kwargs):
    """Create a Docker container via the low-level API."""
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


def create_high_level(*args, **kwargs):
    """Create a Docker container via the high-level API."""
    container = common.CLIENT.containers.create(*args, **kwargs)

    CONTAINERS.append(container)
    return container


def logs(*args: Any, **kwargs: Any) -> Any:
    """Show logs of a Docker container."""
    return common.API_CLIENT.logs(*args, **kwargs)


def remove(container: Container, *args: Any, **kwargs: Any) -> Any:
    """Remove a Docker container."""
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


def run(name: str, *args, **kwargs):
    """Run a Docker container."""
    logs = common.CLIENT.containers.run(name=name, **kwargs)
    container = common.CLIENT.containers.get(name)
    CONTAINERS.append(container)

    return (container, logs)

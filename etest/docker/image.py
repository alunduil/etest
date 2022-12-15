"""Docker Image."""

import logging
from pathlib import Path
from typing import Any

import docker
from docker.models.images import Image

from etest.docker import common

_LOGGER = logging.getLogger()


def build(path: Path, *args: Any, **kwargs: Any) -> Image:
    """Build a docker image."""
    image, logs = common.CLIENT.images.build(path=str(path.parent), *args, **kwargs)

    for line in logs:
        _LOGGER.debug(line.get("stream"))

    return image


def remove(*args: Any, **kwargs: Any) -> Any:
    """Remove a Docker image."""
    return common.API_CLIENT.remove_image(*args, **kwargs)


def pull(image_name: str) -> None:
    """Pull Docker image by name and clean up any old images."""
    image_id = None

    try:
        image_id = common.API_CLIENT.inspect_image(image_name)["Id"]
    except docker.errors.APIError as error:
        if error.response.status_code != 404:
            raise error

    repository, tag = image_name.split(":")

    common.API_CLIENT.pull(repository=repository, tag=tag)

    if (
        image_id is not None
        and image_id != common.API_CLIENT.inspect_image(image_name)["Id"]
    ):
        try:
            common.API_CLIENT.remove_image(image_id)
        except docker.errors.APIError as error:
            if error.response.status_code not in [404, 409]:
                raise error


def push(tag: str, repository: str = "ebuildtest/etest", *args: Any, **kwargs: Any) -> Any:
    """Push a built image to dockerhub."""
    return common.CLIENT.images.push(repository=repository, tag=tag, *args, **kwargs)

# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import docker
import threading

from docker import Client  # flake8: noqa — import to propogate into etest

DOCKER_PULL_LOCK = threading.Lock()


def pull(image_name):
    '''Pull Docker image by name and clean up any old images.

    '''

    try:
        if DOCKER_PULL_LOCK.acquire(blocking = False):
            client = docker.Client()

            image_id = None

            try:
                image_id = client.inspect_image(image_name)['Id']
            except docker.errors.APIError as error:
                if error.response.status_code != 404:
                    raise error

            repository, tag = image_name.split(':')

            client.pull(repository = repository, tag = tag)

            if image_id is not None and image_id != client.inspect_image(image_name)['Id']:
                client.remove_image(image_id)
        else:
            # Wait for the thread doing the pulling to finish.
            DOCKER_PULL_LOCK.acquire()
    finally:
        DOCKER_PULL_LOCK.release()

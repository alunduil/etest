# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import docker

from etest.docker import common


def remove(*args, **kwargs):
    return common.CLIENT.remove_image(*args, **kwargs)


def pull(image_name):
    '''Pull Docker image by name and clean up any old images.'''

    image_id = None

    try:
        image_id = common.CLIENT.inspect_image(image_name)['Id']
    except docker.errors.APIError as error:
        if error.response.status_code != 404:
            raise error

    repository, tag = image_name.split(':')

    common.CLIENT.pull(repository = repository, tag = tag)

    if image_id is not None and image_id != common.CLIENT.inspect_image(image_name)['Id']:
        try:
            common.CLIENT.remove_image(image_id)
        except docker.errors.APIError as error:
            if error.response.status_code not in [ 404, 409 ]:
                raise error

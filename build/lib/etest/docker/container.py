# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from etest.docker import common

CONTAINERS = []
CREATE = True


def commit(*args, **kwargs):
    return common.CLIENT.commit(*args, **kwargs)


def create(*args, **kwargs):
    return common.CLIENT.create_container(*args, **kwargs)


def logs(*args, **kwargs):
    return common.CLIENT.logs(*args, **kwargs)


def remove(container, *args, **kwargs):
    CONTAINERS.remove(container)
    return common.CLIENT.remove_container(container, *args, **kwargs)


def start(container, *args, **kwargs):
    if not CREATE:
        return False

    CONTAINERS.append(container)
    common.CLIENT.start(container, *args, **kwargs)

    return True


def stop(container, *args, **kwargs):
    return common.CLIENT.stop(container, *args, **kwargs)


def wait(*args, **kwargs):
    return common.CLIENT.wait(*args, **kwargs)

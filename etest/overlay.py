# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import logging
import os

from etest import ebuild

logger = logging.getLogger(__name__)


class Overlay(object):
    @property
    @functools.lru_cache(1)
    def directory(self):
        _ = os.getcwd()

        while _ != '/':
            if os.path.exists(os.path.join(_, 'metadata', 'layout.conf')):
                break

            _ = os.path.dirname(_)
        else:
            raise InvalidOverlayError('not in a valid ebuild repository directory')

        return _

    @property
    def ebuilds(self):
        for path, directories, files in os.walk(self.directory):
            if 'files' in directories:
                directories.remove('files')

            for _ in files:
                if _.endswith('.ebuild'):
                    yield ebuild.Ebuild(os.path.relpath(os.path.join(path, _), self.directory), self)


class InvalidOverlayError(RuntimeError):
    pass

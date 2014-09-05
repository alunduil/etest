# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import os

from etest import ebuild

logger = logging.getLogger(__name__)


class Overlay(object):
    @property
    def directory(self):
        if not hasattr(self, '_directory'):
            _ = os.getcwd()

            while _ != '/':
                logger.debug('current path: %s', _)

                if os.path.exists(os.path.join(_, 'profiles', 'repo_name')) and os.path.exists(os.path.join(_, 'metadata', 'layout.conf')):
                    self._directory = _
                    break

                _ = os.path.dirname(_)
            else:
                raise InvalidOverlayError('not in a portage tree or overlay directory')

        return self._directory

    @property
    def ebuilds(self):
        if not hasattr(self, '_ebuilds'):
            self._ebuilds = []

            for path, directories, files in os.walk(self.directory):
                if 'files' in directories:
                    directories.remove('files')

                self._ebuilds.extend([ ebuild.Ebuild(os.path.relpath(os.path.join(path, _), self.directory), self.directory) for _ in files if _.endswith('.ebuild') ])

        return self._ebuilds


class InvalidOverlayError(RuntimeError):
    pass

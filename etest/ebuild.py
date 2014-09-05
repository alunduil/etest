# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import os

from etest import helpers

logger = logging.getLogger(__name__)


class Ebuild(object):
    def __init__(self, path, overlay):
        self.path = path
        self.overlay = overlay

        self.parsed = False

    @property
    def name(self):
        if not hasattr(self, '_name'):
            logger.debug('self.path: %s', self.path)

            self._name = os.path.dirname(self.path)

        return self._name

    @property
    def use_flags(self):
        if not hasattr(self, '_use_flags'):
            self._use_flags = self.parse()['IUSE']

        return self._use_flags

    def parse(self):
        '''Convert ebuild file into a dictionary, mapping variables to values.

        Parses the ebuild file and constructs a dictionary that maps the
        variables to their values.

        .. note::
            parse() caches the results and will not re-read the ebuild file

        Returns
        -------

        Dictionary whose keys are variables in the associated ebuild.
        
        '''

        if not self.parsed:
            self._parse = {}

            logger.debug('overlay_path: %s', self.overlay.directory)

            with open(os.path.join(self.overlay.directory, self.path), 'r') as fh:
                self._parse = helpers.bash_to_dict(fh.read())

            self.parsed = True

        return self._parse

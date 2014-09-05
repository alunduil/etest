# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

from etest import overlay

logger = logging.getLogger(__name__)


class Tests(object):
    def __init__(self, ebuilds = ()):
        self.overlay = overlay.Overlay()

# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import unittest
import os

from etest import overlay

from test_etest.test_fixtures import FIXTURES_DIRECTORY


class TestOverlayWithNonEmptyOverlay(unittest.TestCase):
    def setUp(self):
        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(os.path.join(FIXTURES_DIRECTORY, 'overlay'))

    def test_nonempty_overlay_directory_detection(self):
        '''overlay.Overlay().directory—nonempty overlay'''

        self.overlay = overlay.Overlay()

        self.assertEqual(os.path.join(FIXTURES_DIRECTORY, 'overlay'), self.overlay.directory)

    def test_nonempty_overlay_nonempty_ebuilds(self):
        '''len(overlay.Overlay().ebuilds) != 0—nonempty overlay'''

        self.overlay = overlay.Overlay()

        self.assertEqual(1, len(self.overlay.ebuilds))

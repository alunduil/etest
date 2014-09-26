# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import unittest

from test_etest.test_common.test_overlay import TestWithEmptyOverlay

from etest import overlay


class TestOverlayWithInvalidOverlay(unittest.TestCase):
    def test_invalid_overlay(self):
        '''overlay.Overlay()—invalid overlay'''

        self.overlay = overlay.Overlay()

        self.assertRaises(overlay.InvalidOverlayError, getattr, self.overlay, 'directory')


class TestOverlayWithEmptyOverlay(TestWithEmptyOverlay):
    def test_empty_overlay_directory_detection(self):
        '''overlay.Overlay().directory—empty overlay'''

        self.overlay = overlay.Overlay()

        self.assertEqual(self.mocked_directory, self.overlay.directory)

    def test_empty_overlay_empty_ebuilds(self):
        '''len(overlay.Overlay().ebuilds) == 0—empty overlay'''
        self.overlay = overlay.Overlay()

        self.assertEqual(0, len(self.overlay.ebuilds))

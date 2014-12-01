# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

from test_etest.test_common import BaseEmptyOverlayTest
from test_etest.test_common import BaseFixtureOverlayTest
from test_etest.test_common.test_overlay import BaseOverlayTest
from test_etest.test_fixtures import FIXTURES_DIRECTORY

from etest import overlay


class InvalidOverlayUnitTest(BaseOverlayTest):
    def test_invalid_overlay(self):
        '''overlay.Overlay()—invalid overlay'''

        self.assertRaises(overlay.InvalidOverlayError, getattr, self.overlay, 'directory')


class ValidEmptyOverlayUnitTest(BaseOverlayTest, BaseEmptyOverlayTest):
    def test_empty_overlay_discovery(self):
        '''overlay.Overlay().directory—empty overlay'''

        self.assertEqual(self.overlay.directory, self.mocked_directory)

    def test_empty_overlay_ebuilds(self):
        '''len(list(overlay.Overlay().ebuilds)) == 0—empty overlay'''

        self.assertEqual(0, len(list(self.overlay.ebuilds)))


class ValidNonEmptyOverlayUnitTest(BaseOverlayTest, BaseFixtureOverlayTest):
    def test_nonempty_overlay_discovery(self):
        '''overlay.Overlay().directory—nonempty overlay'''

        self.assertEqual(self.overlay.directory, os.path.join(FIXTURES_DIRECTORY, 'overlay'))

    def test_nonempty_overlay_ebuilds(self):
        '''len(list(overlay.Overlay().ebuilds)) == 1—nonempty overlay'''

        self.assertEqual(1, len(list(self.overlay.ebuilds)))

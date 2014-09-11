# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import unittest
import os
import tempfile

from etest import overlay

from test_etest.test_fixtures import FIXTURES_DIRECTORY


class TestOverlayWithInvalidOverlay(unittest.TestCase):
    def test_invalid_overlay(self):
        '''overlay.Overlay()—invalid overlay'''

        self.overlay = overlay.Overlay()

        self.assertRaises(overlay.InvalidOverlayError, getattr, self.overlay, 'directory')


class TestOverlayWithEmptyOverlay(unittest.TestCase):
    def setUp(self):
        self.mocked_directory = tempfile.mkdtemp()
        self.addCleanup(os.rmdir, self.mocked_directory)

        _ = os.path.join(self.mocked_directory, 'profiles')
        os.mkdir(_)
        self.addCleanup(os.rmdir, _)

        _ = os.path.join(self.mocked_directory, 'profiles', 'repo_name')
        with open(_, 'w') as fh:
            fh.write('etest')
        self.addCleanup(os.remove, _)

        _ = os.path.join(self.mocked_directory, 'metadata')
        os.mkdir(_)
        self.addCleanup(os.rmdir, _)

        _ = os.path.join(self.mocked_directory, 'metadata', 'layout.conf')
        with open(_, 'w') as fh:
            fh.write('masters = gentoo')
        self.addCleanup(os.remove, _)

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(self.mocked_directory)

    def test_empty_overlay_directory_detection(self):
        '''overlay.Overlay().directory—empty overlay'''

        self.overlay = overlay.Overlay()

        self.assertEqual(self.mocked_directory, self.overlay.directory)

    def test_empty_overlay_empty_ebuilds(self):
        '''len(overlay.Overlay().ebuilds) == 0—empty overlay'''
        self.overlay = overlay.Overlay()

        self.assertEqual(0, len(self.overlay.ebuilds))


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

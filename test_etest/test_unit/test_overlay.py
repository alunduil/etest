# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import os
import tempfile
import unittest

from test_etest.test_common.test_overlay import BaseOverlayTest
from test_etest.test_fixtures import FIXTURES_DIRECTORY

from etest import overlay


class InvalidOverlayUnitTest(BaseOverlayTest):
    def test_invalid_overlay(self):
        '''overlay.Overlay()—invalid overlay'''

        self.assertRaises(overlay.InvalidOverlayError, getattr, self.overlay, 'directory')


class ValidEmptyOverlayUnitTest(BaseOverlayTest):
    def setUp(self):
        super().setUp()

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

    def test_empty_overlay_discovery(self):
        '''overlay.Overlay().directory—empty overlay'''

        self.assertEqual(self.overlay.directory, self.mocked_directory)

    def test_empty_overlay_ebuilds(self):
        '''len(list(overlay.Overlay().ebuilds)) == 0—empty overlay'''

        self.assertEqual(0, len(list(self.overlay.ebuilds)))


class ValidNonEmptyOverlayUnitTest(BaseOverlayTest):
    def setUp(self):
        super().setUp()

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(os.path.join(FIXTURES_DIRECTORY, 'overlay'))

    def test_nonempty_overlay_discovery(self):
        '''overlay.Overlay().directory—nonempty overlay'''

        self.assertEqual(self.overlay.directory, os.path.join(FIXTURES_DIRECTORY, 'overlay'))

    def test_nonempty_overlay_ebuilds(self):
        '''len(list(overlay.Overlay().ebuilds)) == 1—nonempty overlay'''

        self.assertEqual(1, len(list(self.overlay.ebuilds)))

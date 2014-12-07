# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import logging
import os
import tempfile

from test_etest.test_common import BaseEtestTest
from test_etest.test_fixtures import FIXTURES_DIRECTORY

from etest import overlay


logger = logging.getLogger(__name__)


class BaseOverlayTest(BaseEtestTest):
    mocks_mask = set()
    mocks = set()

    def setUp(self):
        super().setUp()

        self.mock_ebuild()

        self.overlay = overlay.Overlay()


class InvalidOverlayUnitTest(BaseOverlayTest):
    def test_invalid_overlay(self):
        '''overlay.Overlay()—invalid overlay'''

        self.assertRaises(overlay.InvalidOverlayError, getattr, self.overlay, 'directory')


class ValidEmptyOverlayUnitTest(BaseOverlayTest):
    def setUp(self):
        super().setUp()

        self.mocked_directory = tempfile.mkdtemp()
        self.addCleanup(os.rmdir, self.mocked_directory)

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

        self.mocked_directory = os.path.join(FIXTURES_DIRECTORY, 'overlay')

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(self.mocked_directory)

    def test_nonempty_overlay_discovery(self):
        '''overlay.Overlay().directory—nonempty overlay'''

        self.assertEqual(self.overlay.directory, self.mocked_directory)

    def test_nonempty_overlay_ebuilds(self):
        '''len(list(overlay.Overlay().ebuilds)) == 1—nonempty overlay'''

        self.assertEqual(1, len(list(self.overlay.ebuilds)))


class ValidNonEmptyOverlaySubdirectoryUnitTest(BaseOverlayTest):
    def setUp(self):
        super().setUp()

        self.mocked_overlay_directory = os.path.join(FIXTURES_DIRECTORY, 'overlay')
        self.mocked_directory = os.path.join(self.mocked_overlay_directory, 'app-portage', 'etest')

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(self.mocked_directory)

    def test_nonempty_overlay_discovery(self):
        '''overlay.Overlay().directory—nonempty overlay,subdirectory'''

        self.assertEqual(self.overlay.directory, self.mocked_overlay_directory)

    def test_nonempty_overlay_ebuilds(self):
        '''len(list(overlay.Overlay().ebuilds)) == 1—nonempty overlay,subdirectory'''

        self.assertEqual(1, len(list(self.overlay.ebuilds)))

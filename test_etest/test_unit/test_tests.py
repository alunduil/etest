# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import logging
import os
import tempfile
import unittest

from test_etest.test_fixtures import FIXTURES_DIRECTORY

from etest import tests

logger = logging.getLogger(__name__)


class TestTestsWithInvalidOverlay(unittest.TestCase):
    def test_invalid_overlay(self):
        '''tests.Tests()—invalid overlay'''

        self.assertRaises(tests.InvalidOverlayError, tests.Tests)


class TestTestsWithEmptyOverlay(unittest.TestCase):
    def setUp(self):
        _ = tempfile.mkdtemp()
        self.addCleanup(os.rmdir, _)

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(_)

    def test_empty_overlay(self):
        '''tests.Tests()—empty overlay'''

        self.tests = tests.Tests()

        self.assertEqual(0, len(self.tests))


class TestTestsWithNonEmptyOverlay(unittest.TestCase):
    def setUp(self):
        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(os.path.join(FIXTURES_DIRECTORY, 'overlay'))

    def test_nonempty_overlay(self):
        '''tests.Tests()—nonempty overlay'''

        self.tests = tests.Tests()

        self.assertEqual(3, len(self.tests))

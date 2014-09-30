# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import os
import unittest

from test_etest.test_common.test_overlay import TestWithEmptyOverlay

from etest import tests
from etest.overlay import InvalidOverlayError

logger = logging.getLogger(__name__)


class TestTestsWithInvalidOverlay(unittest.TestCase):
    def test_invalid_overlay(self):
        '''tests.Tests()—invalid overlay'''

        self.assertRaises(InvalidOverlayError, tests.Tests)


class TestTestsWithEmptyOverlay(TestWithEmptyOverlay):
    def test_empty_overlay(self):
        '''tests.Tests()—empty overlay'''

        self.tests = tests.Tests()

        self.assertEqual(0, len(self.tests.tests))

    def test_ebuild_filter(self):
        '''tests.Tests().ebuild_filter'''

        self.tests = tests.Tests()

        self.assertEqual((), self.tests.ebuild_filter)

    def test_ebuild_filter(self):
        '''tests.Tests(app-portage/etest).ebuild_filter'''

        self.tests = tests.Tests(('app-portage/etest',))

        self.assertEqual(['app-portage/etest',], self.tests.ebuild_filter)

# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import unittest
import os

from test_etest.test_fixtures import FIXTURES_DIRECTORY

from etest import tests


class TestTestsWithNonEmptyOverlay(unittest.TestCase):
    def setUp(self):
        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(os.path.join(FIXTURES_DIRECTORY, 'overlay'))

    def test_nonempty_overlay(self):
        '''tests.Tests()—nonempty overlay'''

        self.tests = tests.Tests()

        self.assertEqual(2, len(list(self.tests.tests)))

    def test_ebuild_filter(self):
        '''tests.Tests().ebuild_filter'''

        self.tests = tests.Tests()

        self.assertEqual([], self.tests.ebuild_filter)

    def test_ebuild_filter_subdirectory(self):
        '''tests.Tests().ebuild_filter—subdirectory'''

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(os.path.join(FIXTURES_DIRECTORY, 'overlay', 'app-portage', 'etest'))

        self.tests = tests.Tests()

        self.assertEqual(['app-portage/etest', ], self.tests.ebuild_filter)

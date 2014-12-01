# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import os
import unittest

from test_etest.test_common import BaseEmptyOverlayTest
from test_etest.test_common import BaseFixtureOverlayTest
from test_etest.test_common.test_tests import BaseTestMetaTest
from test_etest.test_common.test_tests import BaseTestTest
from test_etest.test_common.test_tests import BaseTestsTest
from test_etest.test_fixtures import FIXTURES_DIRECTORY

from etest.tests import Tests
from etest.overlay import InvalidOverlayError


class TestUnitTest(BaseTestTest, metaclass = BaseTestMetaTest):
    mocks_mask = set().union(BaseTestTest.mocks_mask)
    mocks = set().union(BaseTestTest.mocks)


class TestsWithInvalidOverlayTest(BaseTestsTest):
    def test_invalid_overlay(self):
        '''tests.Tests()—invalid overlay'''

        if self.is_mocked_overlay:
            type(self.mocked_overlay).directory = os.getcwd()

        self.assertRaises(InvalidOverlayError, Tests)


class ValidEmptyTestsUnitTest(BaseTestsTest, BaseEmptyOverlayTest):
    def setUp(self):
        super().setUp()

        if self.is_mocked_overlay:
            type(self.mocked_overlay).directory = unittest.mock.PropertyMock(return_value = self.mocked_directory)

    def test_empty_tests(self):
        '''len(list(tests.Tests().tests)) == 0—empty overlay'''

        self.tests = Tests()
        self.assertEqual(0, len(list(self.tests.tests)))

class ValidNonEmptyTestsUnitTest(BaseTestsTest, BaseFixtureOverlayTest):
    def setUp(self):
        super().setUp()

        if self.is_mocked_overlay:
            type(self.mocked_overlay).directory = unittest.mock.PropertyMock(return_value = self.mocked_directory)

    def test_nonempty_tests_empty_filter(self):
        '''len(list(tests.Tests().tests)) == 2—nonempty overlay'''

        self.tests = Tests()
        self.assertEqual(2, len(list(self.tests.tests)))

    def test_nonempty_tests_nonempty_filter(self):
        '''len(list(tests.Tests(ebuild_selector = ('app-portage/etest',)).tests)) == 2—nonempty overlay'''

        self.tests = Tests(('app-portage/etest'),)
        self.assertEqual(2, len(list(self.tests.tests)))

    def test_nonempty_tests_subdirectory(self):
        '''len(list(tests.Tests().tests)) == 2—nonempty overlay,subdirectory'''

        self.mocked_directory = os.path.join(FIXTURES_DIRECTORY, 'overlay', 'app-portage', 'etest')

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(self.mocked_directory)

        if self.is_mocked_overlay:
            type(self.mocked_overlay).directory = unittest.mock.PropertyMock(return_value = self.mocked_directory)

        self.tests = Tests()
        self.assertEqual(2, len(list(self.tests.tests)))

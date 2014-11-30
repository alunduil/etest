# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import logging
import unittest
import unittest.mock

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

        self.assertEqual(0, len(list(self.tests.tests)))

    def test_ebuild_filter_empty(self):
        '''tests.Tests().ebuild_filter'''

        self.tests = tests.Tests()

        self.assertEqual([], self.tests.ebuild_filter)

    def test_ebuild_filter_nonempty(self):
        '''tests.Tests(app-portage/etest).ebuild_filter'''

        self.tests = tests.Tests(('app-portage/etest',))

        self.assertEqual(['app-portage/etest', ], self.tests.ebuild_filter)


class TestTestProperties(unittest.TestCase):
    def setUp(self):
        self.mocked_ebuild = unittest.mock.MagicMock()

        type(self.mocked_ebuild).cpv = unittest.mock.PropertyMock(return_value = '=app-portage/ebuild-9999')

    def test_name_without_test(self):
        '''tests.Test(ebuild.Ebuild('app-portage/ebuild-9999'), use_flags = ('doc', 'examples')).name'''

        self.test = tests.Test(self.mocked_ebuild, use_flags = ('doc', 'examples'))

        self.assertEqual('=app-portage/ebuild-9999[doc,examples]', self.test.name)

    def test_name_with_test(self):
        '''tests.Test(ebuild.Ebuild('app-portage/ebuild-9999'), use_flags = ('doc', 'examples'), test = True).name'''

        self.test = tests.Test(self.mocked_ebuild, use_flags = ('doc', 'examples'), test = True)

        self.assertEqual('=app-portage/ebuild-9999[doc,examples,test]', self.test.name)

    def test_time(self):
        '''tests.Test(ebuild.Ebuild('app-portage/ebuild-9999'), use_flags = ('doc', 'examples')).time'''

        self.test = tests.Test(self.mocked_ebuild, use_flags = ('doc', 'examples'))

        self.assertEqual(datetime.timedelta(0), self.test.time)

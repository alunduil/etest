# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_etest.test_common.test_tests import BaseTestMetaTest
from test_etest.test_common.test_tests import BaseTestTest


class TestUnitTest(BaseTestTest, metaclass = BaseTestMetaTest):
    mocks_mask = set().union(BaseTestTest.mocks_mask)
    mocks = set().union(BaseTestTest.mocks)


# TODO: Add Tests tests

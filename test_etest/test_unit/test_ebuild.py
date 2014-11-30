# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_etest.test_common.test_ebuild import BaseEbuildMetaTest
from test_etest.test_common.test_ebuild import BaseEbuildTest


class EbuildUnitTest(BaseEbuildTest, metaclass = BaseEbuildMetaTest):
    mocks_mask = set().union(BaseEbuildTest.mocks_mask)
    mocks = set().union(BaseEbuildTest.mocks)

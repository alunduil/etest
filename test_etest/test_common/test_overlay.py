# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import re
import unittest
import unittest.mock

from test_etest import test_helpers
from test_etest.test_common import BaseEtestTest

from etest import overlay

logger = logging.getLogger(__name__)


class BaseOverlayTest(BaseEtestTest):
    mocks_mask = set()
    mocks = set()

    def setUp(self):
        super().setUp()

        self.mock_ebuild()

        self.overlay = overlay.Overlay()

    mocks.add('ebuild')

    @test_helpers.mocker('ebuild')
    def mock_ebuild(self):
        logger.debug('mocking %s', self.real_module + '.ebuild')
        _ = unittest.mock.patch(self.real_module + '.ebuild')
        self.mocked_ebuild = _.start()
        self.addCleanup(_.stop)

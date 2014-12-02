# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

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

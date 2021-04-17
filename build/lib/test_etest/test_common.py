# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import re
import unittest

from test_etest import test_helpers

logger = logging.getLogger(__name__)


class BaseEtestTest(unittest.TestCase):
    mocks_mask = set()
    mocks = set()

    @property
    def real_module(self):
        return re.sub(r'\.[^.]+', '', self.__module__.replace('test_', ''), 1)

    def _patch(self, name):
        logger.debug('mocking %s', self.real_module + '.' + name)
        _ = unittest.mock.patch(self.real_module + '.' + name)
        setattr(self, 'mocked_' + name.replace('.', '_').strip('_'), _.start())
        self.addCleanup(_.stop)

    mocks.add('ebuild')

    @test_helpers.mock('ebuild')
    def mock_ebuild(self):
        self._patch('ebuild')

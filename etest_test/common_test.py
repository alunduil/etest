"""Common testing bits."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import re
import unittest
from typing import Set

from etest_test import helpers_test

logger = logging.getLogger(__name__)


class BaseEtestTest(unittest.TestCase):
    """Base Etest Test."""

    mocks_mask: Set = set()
    mocks: Set = set()

    @property
    def real_module(self):
        """Name of the real module."""
        return re.sub(r"\.[^.]+", "", self.__module__.replace("_test", ""), 1)

    def _patch(self, name):
        logger.debug("mocking %s", self.real_module + "." + name)
        _ = unittest.mock.patch(self.real_module + "." + name)
        setattr(self, "mocked_" + name.replace(".", "_").strip("_"), _.start())
        self.addCleanup(_.stop)

    mocks.add("ebuild")

    @helpers_test.mock("ebuild")
    def mock_ebuild(self):
        """Mock ebuild."""
        self._patch("ebuild")

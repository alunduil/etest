"""Fixture tests."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os
from typing import Dict

from etest_test import helpers_test

TESTS: Dict = {}

helpers_test.import_directory(__name__, os.path.dirname(__file__))

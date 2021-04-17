# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

from test_etest import test_helpers

EBUILDS = {}

test_helpers.import_directory(__name__, os.path.dirname(__file__))

"""Plus operator to find arguments."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "04ec19a6-834e-4f46-88a4-e947a90826ce",
    "description": "plus operator in find arguments",
    "text": textwrap.dedent(
        """
        find "${D}" -name '*.la' -exec rm -f '{}' +
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)
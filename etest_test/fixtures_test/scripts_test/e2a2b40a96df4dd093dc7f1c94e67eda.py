"""Assign empty string."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "e2a2b40a96df4dd093dc7f1c94e67eda",
    "description": "assign empty string",
    "text": textwrap.dedent(
        """
        IUSE=""
        """,
    ),
    "symbols": {
        "IUSE": "",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

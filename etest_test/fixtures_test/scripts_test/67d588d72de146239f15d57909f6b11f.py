"""Nested curly braces."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "67d588d7-2de1-4623-9f15-d57909f6b11f",
    "description": "nested curly braces",
    "text": textwrap.dedent(
        """
        local CTARGET=${CTARGET:-${CHOST}}
        """,
    ),
    "symbols": {
        "CTARGET": "${CTARGET:-${CHOST}}",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)
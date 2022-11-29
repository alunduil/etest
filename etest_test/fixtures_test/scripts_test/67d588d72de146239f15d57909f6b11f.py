"""Nested curly braces."""
# pylint: disable=C0103

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

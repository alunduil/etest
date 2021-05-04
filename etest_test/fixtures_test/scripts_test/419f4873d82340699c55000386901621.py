"""Multiline array assignment."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "419f4873d82340699c55000386901621",
    "description": "multiline array assignment",
    "text": textwrap.dedent(
        """
        local FOO=(
            bar
        )
        """,
    ),
    "symbols": {
        "FOO": ("bar",),
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

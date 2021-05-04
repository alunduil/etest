"""Assign empty string."""

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

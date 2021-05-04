"""Empty text."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "032bfd4400a74dee8d41ac515a56a44b",
    "description": "empty text",
    "text": textwrap.dedent(
        """
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

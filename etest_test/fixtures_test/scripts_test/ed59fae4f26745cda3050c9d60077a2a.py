"""Unadorned curly braces."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "a5f28a1f-930a-482e-b94d-b56fad5984a3",
    "description": "unadorned curly braces",
    "text": textwrap.dedent(
        """
        find "${ED}" -name '*.la' -exec rm -f {} +
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

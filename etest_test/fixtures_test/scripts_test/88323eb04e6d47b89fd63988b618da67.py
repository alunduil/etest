"""Asterisk word token."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "88323eb0-4e6d-47b8-9fd6-3988b618da67",
    "description": "asterisk word token",
    "text": textwrap.dedent(
        """
        dodoc -r *
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

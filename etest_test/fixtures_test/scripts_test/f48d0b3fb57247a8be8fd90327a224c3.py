"""Implicit concatenation of strings."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "f48d0b3fb57247a8be8fd90327a224c3",
    "description": "implicit concatenation of strings",
    "text": textwrap.dedent(
        """
        FOO="bar"baz
        """,
    ),
    "symbols": {
        "FOO": "barbaz",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

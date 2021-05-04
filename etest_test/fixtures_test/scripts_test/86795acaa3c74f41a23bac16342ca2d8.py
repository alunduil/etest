"""Curly brace expansion."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "86795acaa3c74f41a23bac16342ca2d8",
    "description": "curly brace expansion",
    "text": textwrap.dedent(
        """
        FOO=python{2_7,3_3}
        """,
    ),
    "symbols": {
        "FOO": ("python2_7", "python3_3"),
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

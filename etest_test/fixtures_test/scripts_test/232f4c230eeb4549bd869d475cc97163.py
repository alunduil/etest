"""Array variable assignment."""
# pylint: disable=C0103

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "232f4c230eeb4549bd869d475cc97163",
    "description": "array variable assignment",
    "text": textwrap.dedent(
        """
        FOO=( bar )
        """,
    ),
    "symbols": {
        "FOO": ("bar",),
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

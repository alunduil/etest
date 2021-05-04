"""Single variable assignment."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "19310cb9eefb40e3a1a008ab8b9013c8",
    "description": "single variable assignment",
    "text": textwrap.dedent(
        """
        FOO=bar
        """,
    ),
    "symbols": {
        "FOO": "bar",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

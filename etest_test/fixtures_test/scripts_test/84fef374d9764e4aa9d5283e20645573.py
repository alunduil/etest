"""Arguments to functions starting with bang."""
# pylint: disable=C0103

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "d5aaeeee36574cd3bf4ffa100537703d",
    "description": "arguments to functions starting with bang",
    "text": textwrap.dedent(
        """
        use !gtk3
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

"""For over a list of numbers."""
# pylint: disable=C0103

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "41299ea-c663-144e-5aab-cf25fa907aa19",
    "description": "for over a list of numbers",
    "text": textwrap.dedent(
        """
        for i in 1 2 3 4; do
            foo
        done
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

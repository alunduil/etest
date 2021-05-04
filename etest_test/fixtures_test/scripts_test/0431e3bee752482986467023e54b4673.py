"""Single comment."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "0431e3bee752482986467023e54b4673",
    "description": "single comment",
    "text": textwrap.dedent(
        """
        # comment
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

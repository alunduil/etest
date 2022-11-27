"""Single full line comment."""
# pylint: disable=C0103

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "0431e3bee752482986467023e54b4673",
    "description": "single full line comment",
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

"""For loop with unencapsulated word list."""
# pylint: disable=C0103

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "7dacf8800b53497cbbfb13603c46fd64",
    "description": "for loop with unencapsulated word list",
    "text": textwrap.dedent(
        """
        for test in test.py selftest.py selftest2.py; do
            echo foo
        done
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

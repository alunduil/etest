"""Double quote assignment."""
# pylint: disable=C0103

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "6dbeb0b3da5745edbf1388fd722c94dc",
    "description": "double quoted assignment",
    "text": textwrap.dedent(
        """
        FOO="bar bar"
        EGIT_REPO_URI="git://github.com/alunduil/etest.git"
        """,
    ),
    "symbols": {
        "FOO": "bar bar",
        "EGIT_REPO_URI": "git://github.com/alunduil/etest.git",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

"""Number as word token."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "d5aaeeee36574cd3bf4ffa100537703d",
    "description": "number as word token",
    "text": textwrap.dedent(
        """
        pkg_setup() {
            python_set_active_version 2
            python_pkg_setup
        }
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

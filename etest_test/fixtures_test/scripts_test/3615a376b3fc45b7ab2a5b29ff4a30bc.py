"""Quoted subshell."""
# pylint: disable=C0103

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "3615a376-b3fc-45b7-ab2a-5b29ff4a30bc",
    "description": "quoted subshell",
    "text": textwrap.dedent(
        """
        currentamanda="$(set | egrep "^AMANDA_" | grep -v '^AMANDA_ENV_SETTINGS' | xargs)"
        """,
    ),
    "symbols": {
        "currentamanda": "$(set | egrep \"^AMANDA_\" | grep -v '^AMANDA_ENV_SETTINGS' | xargs)",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

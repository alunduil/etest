"""Test with variable in double quotes."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "bb9e1873e781476fa61c80ba0cb144d9",
    "description": "test with variable in double quotes",
    "text": textwrap.dedent(
        """
        if [[ "${LC_ALL}" = "C" ]]; then
            echo
        fi
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

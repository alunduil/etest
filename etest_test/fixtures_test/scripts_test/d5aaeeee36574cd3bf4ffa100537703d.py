"""Assignment of a variable to a variable."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "d5aaeeee36574cd3bf4ffa100537703d",
    "description": "assignment of a variable to a variable",
    "text": textwrap.dedent(
        """
        MY_PN=${PN/-/.}
        """,
    ),
    "symbols": {
        "MY_PN": "${PN/-/.}",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

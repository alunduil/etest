"""Plus operator to find arguments."""
# pylint: disable=C0103

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "04ec19a6-834e-4f46-88a4-e947a90826ce",
    "description": "plus operator in find arguments",
    "text": textwrap.dedent(
        """
        find "${D}" -name '*.la' -exec rm -f '{}' +
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

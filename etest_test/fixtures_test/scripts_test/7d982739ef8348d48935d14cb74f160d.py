"""Function definition."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "7d982739ef8348d48935d14cb74f160d",
    "description": "function definition",
    "text": textwrap.dedent(
        """
        python_test() {
            nosetests || die "Tests failed under ${EPYTHON}"
        }
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

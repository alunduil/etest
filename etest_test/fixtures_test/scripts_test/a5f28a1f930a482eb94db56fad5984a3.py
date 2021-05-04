"""Word with subshell embedded."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "a5f28a1f-930a-482e-b94d-b56fad5984a3",
    "description": "word with subshell embedded",
    "text": textwrap.dedent(
        """
        insinto /usr/$(get_libdir)/crda/
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

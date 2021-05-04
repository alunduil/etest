"""Equals inside quotes."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "90e12d26-fd6d-4485-a1f8-b35716f5fd1e",
    "description": "equals inside quotes",
    "text": textwrap.dedent(
        """
        echo "CONFIG_EAP=y" >> ${CONFIG}
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

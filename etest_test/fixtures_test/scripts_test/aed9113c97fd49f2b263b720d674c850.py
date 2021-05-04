"""Function with subshells."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "aed9113c97fd49f2b263b720d674c850",
    "description": "function with subshells",
    "text": textwrap.dedent(
        """
        src_configure() {
            econf \
                $(use_enable python) \
                $(use_enable java)
        }
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

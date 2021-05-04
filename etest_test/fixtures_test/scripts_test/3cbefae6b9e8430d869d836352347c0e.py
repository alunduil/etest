"""Quoted variable expansions."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "3cbefae6b9e8430d869d836352347c0e",
    "description": "quoted variable expansions",
    "text": textwrap.dedent(
        """
        SRC_URI="mirror://pypi/${MY_PN:0:1}/${MY_PN}/${MY_PN}-${PV}.tar.gz"
        """,
    ),
    "symbols": {
        "SRC_URI": "mirror://pypi/${MY_PN:0:1}/${MY_PN}/${MY_PN}-${PV}.tar.gz",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

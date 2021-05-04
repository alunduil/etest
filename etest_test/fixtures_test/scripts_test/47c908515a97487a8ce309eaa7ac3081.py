"""Dangling double quote."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "40e465907f16472db2828d3998a03ae0",
    "description": "dangling double quote",
    "text": textwrap.dedent(
        """
        FOO="
        """,
    ),
    "symbols": {},
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

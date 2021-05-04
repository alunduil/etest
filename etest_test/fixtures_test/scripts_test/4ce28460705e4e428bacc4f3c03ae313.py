"""Word with an underscore."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "4ce28460-705e-4e42-8bac-c4f3c03ae313",
    "description": "word with an underscore",
    "text": textwrap.dedent(
        """
        MY_P=${PN}_${PV}
        """,
    ),
    "symbols": {
        "MY_P": "${PN}_${PV}",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

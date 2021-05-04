"""Line continuation."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "bec3d10b974e4447853ef59268946fe1",
    "description": "line continuation",
    "text": textwrap.dedent(
        """
        foo \
            continues \
            on
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

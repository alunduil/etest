"""Words with equals without assignment in array."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "d1ec9787-9e85-46d5-81c5-78ce046b8fc1",
    "description": "words with equals without assignment in array",
    "text": textwrap.dedent(
        """
        local mycmakeargs=(
            -DVALA_EXECUTABLE="${VALAC}"
            -DGSETTINGS_COMPILE=OFF
            -DMINIMAL_FLAGS=ON
        )
        """,
    ),
    "symbols": {
        "mycmakeargs": (
            "-DVALA_EXECUTABLE=${VALAC}",
            "-DGSETTINGS_COMPILE=OFF",
            "-DMINIMAL_FLAGS=ON",
        ),
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

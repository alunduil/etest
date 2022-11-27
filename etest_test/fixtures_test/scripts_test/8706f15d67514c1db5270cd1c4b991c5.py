"""Assign keywords."""
# pylint: disable=C0103

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "8706f15d-6751-4c1d-b527-0cd1c4b991c5",
    "description": "assign keywords",
    "text": textwrap.dedent(
        """
        IUSE_LINGUAS=( en da de es fi fr it ja ko nl no pt_BR se zh_CN )
        """,
    ),
    "symbols": {
        "IUSE_LINGUAS": (
            "en",
            "da",
            "de",
            "es",
            "fi",
            "fr",
            "it",
            "ja",
            "ko",
            "nl",
            "no",
            "pt_BR",
            "se",
            "zh_CN",
        ),
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

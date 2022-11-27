"""Escaped character as a word."""
# pylint: disable=C0103

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "14c46139-340a-4ca9-a266-b37a80e74533",
    "description": "escaped character as a word",
    "text": textwrap.dedent(
        r"""
        find bin.* -mindepth 1 -maxdepth 1 -type f -exec dobin '{}' \; || die
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

"""Multiline array assignment."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "419f4873d82340699c55000386901621",
    "description": "multiline array assignment",
    "text": textwrap.dedent(
        """
        local FOO=(
            bar
        )
        """,
    ),
    "symbols": {
        "FOO": ("bar",),
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

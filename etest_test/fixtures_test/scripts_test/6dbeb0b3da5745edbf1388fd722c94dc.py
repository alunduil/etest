"""Double quote assignment."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "6dbeb0b3da5745edbf1388fd722c94dc",
    "description": "double quoted assignment",
    "text": textwrap.dedent(
        """
        FOO="bar bar"
        EGIT_REPO_URI="git://github.com/alunduil/etest.git"
        """,
    ),
    "symbols": {
        "FOO": "bar bar",
        "EGIT_REPO_URI": "git://github.com/alunduil/etest.git",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

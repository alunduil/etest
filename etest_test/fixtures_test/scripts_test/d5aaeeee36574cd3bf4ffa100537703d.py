"""Assignment of a variable to a variable."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "d5aaeeee36574cd3bf4ffa100537703d",
    "description": "assignment of a variable to a variable",
    "text": textwrap.dedent(
        """
        MY_PN=${PN/-/.}
        """,
    ),
    "symbols": {
        "MY_PN": "${PN/-/.}",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

"""Test with variable in double quotes."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "bb9e1873e781476fa61c80ba0cb144d9",
    "description": "test with variable in double quotes",
    "text": textwrap.dedent(
        """
        if [[ "${LC_ALL}" = "C" ]]; then
            echo
        fi
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

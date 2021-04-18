"""Equals inside quotes."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "90e12d26-fd6d-4485-a1f8-b35716f5fd1e",
    "description": "equals inside quotes",
    "text": textwrap.dedent(
        """
        echo "CONFIG_EAP=y" >> ${CONFIG}
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)
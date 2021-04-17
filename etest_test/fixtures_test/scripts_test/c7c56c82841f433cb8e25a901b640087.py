"""Unexpected die."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "c7c56c82-841f-433c-b8e2-5a901b640087",
    "description": "unexpected die",
    "text": textwrap.dedent(
        """
        die
        mv "${WORKDIR}"/${P}-${lang}.po po/${lang}.po || die
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

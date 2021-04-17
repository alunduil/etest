"""Single variable assignment."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "19310cb9eefb40e3a1a008ab8b9013c8",
    "description": "single variable assignment",
    "text": textwrap.dedent(
        """
        FOO=bar
        """,
    ),
    "symbols": {
        "FOO": "bar",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

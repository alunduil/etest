"""Variable value with unquoated equals."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "de2255e260cb47f1ba24c79477fb3ba6",
    "description": "variable value with unquoted equals",
    "text": textwrap.dedent(
        """
        FOO=bar=baz
        """,
    ),
    "symbols": {
        "FOO": "bar=baz",
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

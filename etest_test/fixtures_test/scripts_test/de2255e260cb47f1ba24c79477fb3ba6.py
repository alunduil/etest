"""Variable value with unquoated equals."""

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

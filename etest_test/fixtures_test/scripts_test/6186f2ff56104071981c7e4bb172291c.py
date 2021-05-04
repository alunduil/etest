"""Array without padded parentheses."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "6186f2ff-5610-4071-981c-7e4bb172291c",
    "description": "array without padded parentheses",
    "text": textwrap.dedent(
        """
        python_install_all() {
            use doc && local HTML_DOCS=( doc/build/html/. )
            use examples && local EXAMPLES=(examples/.)

            distutils-r1_python_install_all
        }
        """,
    ),
    "symbols": {
        "HTML_DOCS": ("doc/build/html/.",),
        "EXAMPLES": ("examples/.",),
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

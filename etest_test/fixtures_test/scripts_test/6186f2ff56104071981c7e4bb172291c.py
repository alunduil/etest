"""Array without padded parentheses."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

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

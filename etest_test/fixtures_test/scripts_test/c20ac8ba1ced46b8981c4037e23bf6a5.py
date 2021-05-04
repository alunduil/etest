"""Command containing path argument."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "c20ac8ba1ced46b8981c4037e23bf6a5",
    "description": "command containing path argument",
    "text": textwrap.dedent(
        """
        python_install_all() {
            distutils-r1_python_install_all

            keepdir /etc/holland
        }
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

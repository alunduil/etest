"""Case statement."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "f69c7bff-a8a9-4259-b454-ada7af84a92d",
    "description": "case statement",
    "text": textwrap.dedent(
        """
        case ${EBUILD_PHASE} in
        prepare|configure|compile|install)
            pushd python > /dev/null || die
            distutils_src_${EBUILD_PHASE}
            popd > /dev/null
            ;;
        esac
        """,
    ),
    "symbols": {},
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

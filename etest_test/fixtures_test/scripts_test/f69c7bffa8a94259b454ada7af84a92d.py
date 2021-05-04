"""Case statement."""

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

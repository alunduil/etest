"""If statement with else."""

import textwrap

from etest_test.fixtures_test.scripts_test import SCRIPTS

_ = {
    "uuid": "345a0ace-e573-4538-9c8a-a82171d3d954",
    "description": "if statement with else",
    "text": textwrap.dedent(
        """
        src_configure() {
            local mycmakeargs=(
                $(cmake-utils_use_with semantic-desktop Soprano)
                $(cmake-utils_use_with kipi)
            )
            # Workaround for bug #479510
            if [[ -e ${EPREFIX}/usr/include/${CHOST}/jconfig.h ]]; then
                mycmakeargs+=( -DJCONFIG_H="${EPREFIX}/usr/include/${CHOST}/jconfig.h" )
            fi

            if use semantic-desktop; then
                mycmakeargs+=(-DGWENVIEW_SEMANTICINFO_BACKEND=Nepomuk)
            else
                mycmakeargs+=(-DGWENVIEW_SEMANTICINFO_BACKEND=None)
            fi

            kde4-base_src_configure
        }
        """,
    ),
    "symbols": {
        "mycmakeargs": (
            "$(cmake-utils_use_with semantic-desktop Soprano)",
            "$(cmake-utils_use_with kipi)",
        ),
        "mycmakeargs+": ("-DGWENVIEW_SEMANTICINFO_BACKEND=None",),
    },
    "correct": None,
}

SCRIPTS.setdefault("all", []).append(_)
SCRIPTS.setdefault("bash", []).append(_)

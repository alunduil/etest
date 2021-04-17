# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
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
'''

_ = {
    'uuid': '345a0ace-e573-4538-9c8a-a82171d3d954',

    'description': 'if statement with else',

    'text': _,

    'symbols': {
        'mycmakeargs': (
            '$(cmake-utils_use_with semantic-desktop Soprano)',
            '$(cmake-utils_use_with kipi)',
        ),
        'mycmakeargs+': (
            '-DGWENVIEW_SEMANTICINFO_BACKEND=None',
        ),
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

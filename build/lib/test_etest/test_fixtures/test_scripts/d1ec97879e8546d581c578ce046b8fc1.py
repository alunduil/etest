# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
local mycmakeargs=(
	-DVALA_EXECUTABLE="${VALAC}"
	-DGSETTINGS_COMPILE=OFF
	-DMINIMAL_FLAGS=ON
)
'''

_ = {
    'uuid': 'd1ec9787-9e85-46d5-81c5-78ce046b8fc1',

    'description': 'words with equals without assignment in array',

    'text': _,

    'symbols': {
        'mycmakeargs': (
            '-DVALA_EXECUTABLE=${VALAC}',
            '-DGSETTINGS_COMPILE=OFF',
            '-DMINIMAL_FLAGS=ON',
        ),
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

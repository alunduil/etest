# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
IUSE_LINGUAS=( en da de es fi fr it ja ko nl no pt_BR se zh_CN )
'''

_ = {
    'uuid': '8706f15d-6751-4c1d-b527-0cd1c4b991c5',

    'description': 'assign keywords',

    'text': _,

    'symbols': {
        'IUSE_LINGUAS': (
            'en',
            'da',
            'de',
            'es',
            'fi',
            'fr',
            'it',
            'ja',
            'ko',
            'nl',
            'no',
            'pt_BR',
            'se',
            'zh_CN',
        ),
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

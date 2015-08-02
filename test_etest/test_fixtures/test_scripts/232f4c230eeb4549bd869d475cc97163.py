# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
FOO=( bar )
'''

_ = {
    'uuid': '232f4c230eeb4549bd869d475cc97163',

    'description': 'array variable assignment',

    'text': _,

    'symbols': {
        'FOO': ( 'bar', ),
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

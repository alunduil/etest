# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
FOO=python{2_7,3_3}
'''

_ = {
    'uuid': '86795acaa3c74f41a23bac16342ca2d8',

    'description': 'curly brace expansion',

    'text': _,

    'symbols': {
        'FOO': ( 'python2_7', 'python3_3', ),
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

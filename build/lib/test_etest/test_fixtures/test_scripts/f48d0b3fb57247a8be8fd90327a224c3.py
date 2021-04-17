# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
FOO="bar"baz
'''

_ = {
    'uuid': 'f48d0b3fb57247a8be8fd90327a224c3',

    'description': 'implicit concatenation of strings',

    'text': _,

    'symbols': {
        'FOO': 'barbaz',
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

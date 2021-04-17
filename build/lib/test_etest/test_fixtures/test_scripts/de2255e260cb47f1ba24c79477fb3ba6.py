# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
FOO=bar=baz
'''

_ = {
    'uuid': 'de2255e260cb47f1ba24c79477fb3ba6',

    'description': 'variable value with unquoted equals',

    'text': _,

    'symbols': {
        'FOO': 'bar=baz',
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

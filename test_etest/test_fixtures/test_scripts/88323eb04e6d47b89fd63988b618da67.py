# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
dodoc -r *
'''

_ = {
    'uuid': '88323eb0-4e6d-47b8-9fd6-3988b618da67',

    'description': 'asterisk word token',

    'text': _,

    'symbols': {
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

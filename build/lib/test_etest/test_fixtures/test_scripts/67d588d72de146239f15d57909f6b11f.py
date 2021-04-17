# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
local CTARGET=${CTARGET:-${CHOST}}
'''

_ = {
    'uuid': '67d588d7-2de1-4623-9f15-d57909f6b11f',

    'description': 'nested curly braces',

    'text': _,

    'symbols': {
        'CTARGET': '${CTARGET:-${CHOST}}',
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

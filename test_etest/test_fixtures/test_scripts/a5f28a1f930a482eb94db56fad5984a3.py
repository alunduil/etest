# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
insinto /usr/$(get_libdir)/crda/
'''

_ = {
    'uuid': 'a5f28a1f-930a-482e-b94d-b56fad5984a3',

    'description': 'word with subshell embedded',

    'text': _,

    'symbols': {
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

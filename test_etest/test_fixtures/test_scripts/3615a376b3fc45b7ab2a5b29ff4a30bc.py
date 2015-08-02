# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa — inline bash script with tabs

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
currentamanda="$(set | egrep "^AMANDA_" | grep -v '^AMANDA_ENV_SETTINGS' | xargs)"
'''

_ = {
    'uuid': '3615a376-b3fc-45b7-ab2a-5b29ff4a30bc',

    'description': 'quoted subshell',

    'text': _,

    'symbols': {
        'currentamanda': '$(set | egrep "^AMANDA_" | grep -v \'^AMANDA_ENV_SETTINGS\' | xargs)',
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

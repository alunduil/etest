# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa — inline bash script with tabs

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
SRC_URI="mirror://pypi/${MY_PN:0:1}/${MY_PN}/${MY_PN}-${PV}.tar.gz"
'''

_ = {
    'uuid': '3cbefae6b9e8430d869d836352347c0e',

    'description': 'quoted variable expansions',

    'text': _,

    'symbols': {
        'SRC_URI': 'mirror://pypi/${MY_PN:0:1}/${MY_PN}/${MY_PN}-${PV}.tar.gz',
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

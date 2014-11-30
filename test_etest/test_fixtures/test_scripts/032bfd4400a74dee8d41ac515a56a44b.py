# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
'''[1:-1]

_ = {
    'uuid': '032bfd4400a74dee8d41ac515a56a44b',

    'description': 'empty text',

    'text': _,

    'symbols': {},
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

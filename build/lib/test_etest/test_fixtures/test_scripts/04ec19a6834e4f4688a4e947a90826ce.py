# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.
  
# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
find "${D}" -name '*.la' -exec rm -f '{}' +
'''

_ = {
    'uuid': '04ec19a6-834e-4f46-88a4-e947a90826ce',

    'description': 'plus operator in find arguments',

    'text': _,

    'symbols': {
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

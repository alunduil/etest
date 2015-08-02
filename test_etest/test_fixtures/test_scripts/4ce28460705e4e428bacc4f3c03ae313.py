# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.
  
# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
MY_P=${PN}_${PV}
'''

_ = {
    'uuid': '4ce28460-705e-4e42-8bac-c4f3c03ae313',

    'description': 'word with an underscore',

    'text': _,

    'symbols': {
        'MY_P': '${PN}_${PV}',
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

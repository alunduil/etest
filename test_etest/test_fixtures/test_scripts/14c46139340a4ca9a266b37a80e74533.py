# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.
  
# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
find bin.* -mindepth 1 -maxdepth 1 -type f -exec dobin '{}' \; || die
'''

_ = {
    'uuid': '14c46139-340a-4ca9-a266-b37a80e74533',

    'description': 'escaped character as a word',

    'text': _,

    'symbols': {
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

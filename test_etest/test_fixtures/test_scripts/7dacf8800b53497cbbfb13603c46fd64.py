# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
for test in test.py selftest.py selftest2.py; do
	echo foo
done
'''

_ = {
    'uuid': '7dacf8800b53497cbbfb13603c46fd64',

    'description': 'for loop with unencapsulated word list',

    'text': _,

    'symbols': {},

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

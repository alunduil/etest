# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
pkg_setup() {
	python_set_active_version 2
	python_pkg_setup
}
'''

_ = {
    'uuid': 'd5aaeeee36574cd3bf4ffa100537703d',

    'description': 'number as word token',

    'text': _,

    'symbols': {
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

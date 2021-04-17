# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

# flake8: noqa (inline bash script with tabs)

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
src_configure() {
	econf \
		$(use_enable python) \
		$(use_enable java)
}
'''

_ = {
    'uuid': 'aed9113c97fd49f2b263b720d674c850',

    'description': 'function with subshells',

    'text': _,

    'symbols': {},

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

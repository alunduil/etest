# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_etest.test_fixtures.test_scripts import SCRIPTS

_ = '''
case ${EBUILD_PHASE} in
prepare|configure|compile|install)
	pushd python > /dev/null || die
	distutils_src_${EBUILD_PHASE}
	popd > /dev/null
	;;
esac
'''  # flake8: noqa — inline bash script with tabs

_ = {
    'uuid': 'f69c7bff-a8a9-4259-b454-ada7af84a92d',

    'description': 'case statement',

    'text': _,

    'symbols': {
    },

    'correct': None,
}

SCRIPTS.setdefault('all', []).append(_)
SCRIPTS.setdefault('bash', []).append(_)

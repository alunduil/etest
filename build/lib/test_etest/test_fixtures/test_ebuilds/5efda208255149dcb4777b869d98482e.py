# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_etest.test_fixtures.test_ebuilds import EBUILDS

_ = {
    'uuid': '5efda208-2551-49dc-b477-7b869d98482e',

    'path': 'dev-python/pyrax/pyrax-1.9.3.ebuild',

    'compat': { 'python': ( 'python2_7', ), },
    'cpv': '=dev-python/pyrax-1.9.3',
    'name': 'dev-python/pyrax',
    'restrictions': [],
    'use_flags': [],
    'version': '1.9.3',

    'symbols': {
        'IUSE': '',
        'PYTHON_COMPAT': ( 'python2_7', ),
    },

    'use_flag_sets': (
        (),
    ),
}

EBUILDS.setdefault('all', []).append(_)

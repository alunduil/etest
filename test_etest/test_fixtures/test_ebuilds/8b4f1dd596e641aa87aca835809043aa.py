# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_etest.test_fixtures.test_ebuilds import EBUILDS

_ = {
    'uuid': '8b4f1dd59-6e64-1aa8-7aca-835809043aa',

    'path': 'app-admin/fleet/fleet-9999.ebuild',

    'compat': {},
    'cpv': '=app-admin/fleet-9999',
    'name': 'app-admin/fleet',
    'restrictions': [ 'test', ],
    'use_flags': [ 'doc', 'examples', ],
    'version': '9999',

    'symbols': {
        'IUSE': 'doc examples',
        'RESTRICT': 'test',
    },

    'use_flag_sets': (
        (),
        ( 'doc', ),
        ( 'examples', ),
        ( 'doc', 'examples', ),
    ),
}

EBUILDS.setdefault('all', []).append(_)

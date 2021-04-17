# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_etest.test_fixtures.test_ebuilds import EBUILDS

_ = {
    'uuid': '08a3cac2-fae9-4e3d-8f72-ab3d49266b30',

    'path': 'net-wireless/grimwepa/grimwepa-1.10_p5-r100.ebuild',

    'compat': {},
    'cpv': '=net-wireless/grimwepa-1.10_p5-r100',
    'name': 'net-wireless/grimwepa',
    'restrictions': [],
    'use_flags': [ 'wep', 'extra' ],
    'version': '1.10_p5-r100',

    'symbols': {
        'IUSE': '+wep +extra',
    },

    'use_flag_sets': (
        (),
        ( 'wep', ),
        ( 'extra', ),
        ( 'wep', 'extra', ),
    ),
}

EBUILDS.setdefault('all', []).append(_)

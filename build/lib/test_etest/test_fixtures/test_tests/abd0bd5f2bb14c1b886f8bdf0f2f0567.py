# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_etest.test_fixtures.test_tests import TESTS
from test_etest.test_fixtures.test_ebuilds.eab5f11185a74264acb98eeb95b3238f import _ as ebuild

_ = {
    'uuid': 'abd0bd5f-2bb1-4c1b-886f-8bdf0f2f0567',

    'ebuild': ebuild,

    'with_test_phase': True,
    'base_docker_image': 'alunduil/etest:latest',
    'use_flags': (),

    'name': '=app-portage/etest-9999[test]',

    'commands': [
        ('bash', '-c', 'echo app-portage/etest test >> /etc/portage/package.env', ),
        ('bash', '-c', 'echo app-portage/etest \'-*\'  >> /etc/portage/package.use/etest', ),
        ('bash', '-c', 'emerge -q -f --autounmask-write =app-portage/etest-9999 >/dev/null 2>&1 || true', ),
        ('bash', '-c', 'etc-update --automode -5 >/dev/null 2>&1', ),
        ('emerge', '-q', '--backtrack=130', '=app-portage/etest-9999', ),
    ],

    'environment': {
        'PYTHON_TARGETS': 'python3_3 python3_4 python2_7',
    },
}

TESTS.setdefault('test', []).append(_)

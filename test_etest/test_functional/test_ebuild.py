# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import logging
import os
import unittest
import unittest.mock

from etest import ebuild

from test_etest.test_fixtures import FIXTURES_DIRECTORY

logger = logging.getLogger(__name__)


class TestBaseEbuild(unittest.TestCase):
    def setUp(self):
        self.addCleanup(functools.partial(os.chdir, os.getcwd()))

        os.chdir(os.path.join(FIXTURES_DIRECTORY, 'overlay'))

        self.mocked_overlay = unittest.mock.MagicMock()
        type(self.mocked_overlay).directory = unittest.mock.PropertyMock(return_value = os.getcwd())


class TestEbuildConstructor(TestBaseEbuild):
    def test_constructor(self):
        '''ebuild.Ebuild()'''

        self.ebuild = ebuild.Ebuild(
            path = 'app-portage/etest/etest-9999.ebuild',
            overlay = self.mocked_overlay,
        )


class TestEbuildProperties(TestBaseEbuild):
    def setUp(self):
        super(TestEbuildProperties, self).setUp()

        self.ebuild = ebuild.Ebuild(
            path = 'app-portage/etest/etest-9999.ebuild',
            overlay = self.mocked_overlay,
        )

    def test_name(self):
        '''ebuild.Ebuild().name'''

        logger.debug('self.ebuild.name: %s', self.ebuild.name)

        self.assertEqual('app-portage/etest', self.ebuild.name)

    def test_cpv(self):
        '''ebuild.Ebuild().cpv'''

        logger.debug('self.ebuild.cpv: %s', self.ebuild.cpv)

        self.assertEqual('=app-portage/etest-9999', self.ebuild.cpv)

    def test_version(self):
        '''ebuild.Ebuild().version'''

        logger.debug('self.ebuild.version: %s', self.ebuild.version)

        self.assertEqual('9999', self.ebuild.version)

    def test_compat(self):
        '''ebuild.Ebuild().compat'''

        logger.debug('self.ebuild.compat.keys(): %s', self.ebuild.compat.keys())

        self.assertIn('python', self.ebuild.compat)

        self.assertEqual(( 'python3_3', 'python3_4', ), self.ebuild.compat['python'])

    def test_use_flags(self):
        '''ebuild.Ebuild().use_flags'''

        logger.debug('self.ebuild.use_flags: %s', self.ebuild.use_flags)

        self.assertEqual(1, len(self.ebuild.use_flags))

# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import logging
import mock
import os
import unittest

from etest import ebuild

from test_etest.test_fixtures import FIXTURES_DIRECTORY

logger = logging.getLogger(__name__)


class TestEbuildConstructor(unittest.TestCase):
    def setUp(self):
        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(os.path.join(FIXTURES_DIRECTORY, 'overlay'))

        logger.debug('FIXTURES_DIRECTORY: %s', FIXTURES_DIRECTORY)
        logger.debug('PWD: %s', os.getcwd())

        self.mocked_overlay = mock.MagicMock()
        type(self.mocked_overlay).directory = mock.PropertyMock(return_value = os.getcwd())

    def test_constructor(self):
        '''ebuild.Ebuild()'''

        self.ebuild = ebuild.Ebuild(
            path = 'app-portage/etest/etest-9999.ebuild',
            overlay = self.mocked_overlay,
        )


class TestEbuildProperties(unittest.TestCase):
    def setUp(self):
        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(os.path.join(FIXTURES_DIRECTORY, 'overlay'))

        logger.debug('FIXTURES_DIRECTORY: %s', FIXTURES_DIRECTORY)
        logger.debug('PWD: %s', os.getcwd())

        self.mocked_overlay = mock.MagicMock()
        type(self.mocked_overlay).directory = mock.PropertyMock(return_value = os.getcwd())

        self.ebuild = ebuild.Ebuild(
            path = 'app-portage/etest/etest-9999.ebuild',
            overlay = self.mocked_overlay,
        )

    def test_use_flags(self):
        '''ebuild.Ebuild().use_flags'''

        self.assertEqual(0, len(self.ebuild.use_flags))


class TestEbuildParse(unittest.TestCase):
    def setUp(self):
        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(os.path.join(FIXTURES_DIRECTORY, 'overlay'))

        logger.debug('FIXTURES_DIRECTORY: %s', FIXTURES_DIRECTORY)
        logger.debug('PWD: %s', os.getcwd())

        self.mocked_overlay = mock.MagicMock()
        type(self.mocked_overlay).directory = mock.PropertyMock(return_value = os.getcwd())

        self.ebuild = ebuild.Ebuild(
            path = 'app-portage/etest/etest-9999.ebuild',
            overlay = self.mocked_overlay,
        )

    def test_parse(self):
        '''ebuild.Ebuild().parse()'''
        
        self.assertIsInstance(self.ebuild.parse(), dict)

    def test_parse_iuse(self):
        '''ebuild.Ebuild.parse()['IUSE']'''

        self.assertIn('IUSE', self.ebuild.parse())
        self.assertEqual(['test'], self.ebuild.parse()['IUSE'])

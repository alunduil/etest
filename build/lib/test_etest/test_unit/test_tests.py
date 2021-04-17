# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import datetime
import functools
import logging
import os
import unittest
import unittest.mock

from test_etest import test_helpers
from test_etest.test_common import BaseEtestTest
from test_etest.test_fixtures import FIXTURES_DIRECTORY
from test_etest.test_fixtures.test_ebuilds import EBUILDS
from test_etest.test_fixtures.test_tests import TESTS

from etest import tests

logger = logging.getLogger(__name__)


class BaseTestMetaTest(type):
    def __init__(cls, name, bases, dct):
        super(BaseTestMetaTest, cls).__init__(name, bases, dct)

        def gen_constructor_case(test):
            kwargs = {
                'base_docker_image': test['base_docker_image'],
                'with_test_phase': test['with_test_phase'],
            }
            kwargs.setdefault('use_flags', test.get('use_flags', []))

            def case(self):
                self.test = tests.Test(
                    self.mocked_ebuild,
                    **kwargs
                )

                self.assertEqual(self.test.ebuild, self.mocked_ebuild)
                self.assertEqual(self.test.with_test_phase, test['with_test_phase'])
                self.assertEqual(self.test.use_flags, test['use_flags'])
                self.assertFalse(self.test.failed)
                self.assertIsNone(self.test.failed_command)
                self.assertEqual(self.test.time, datetime.timedelta(0))
                self.assertEqual(self.test.output, '')
                self.assertEqual(self.test.base_docker_image, test['base_docker_image'])

            case.__name__ = 'test_constructor_' + str(test['uuid'])
            case.__doc__ = 'test.Test(mocked_ebuild, with_test_phase = {0[with_test_phase]}, base_docker_image = {0[base_docker_image]}, use_flags = {0[use_flags]})'.format(kwargs)

            return case

        def gen_property_case(test, prop):
            kwargs = {
                'base_docker_image': test['base_docker_image'],
                'with_test_phase': test['with_test_phase'],
            }
            kwargs.setdefault('use_flags', test.get('use_flags', []))

            def case(self):
                type(self.mocked_ebuild).compat = unittest.mock.PropertyMock(return_value = test['ebuild']['compat'])
                type(self.mocked_ebuild).cpv = unittest.mock.PropertyMock(return_value = test['ebuild']['cpv'])
                type(self.mocked_ebuild).name = unittest.mock.PropertyMock(return_value = test['ebuild']['name'])

                self.test = tests.Test(
                    self.mocked_ebuild,
                    **kwargs
                )

                self.assertEqual(getattr(self.test, prop), test[prop])

            case.__name__ = 'test_property_' + prop + '_' + str(test['uuid'])
            case.__doc__ = 'test.Test(mocked_ebuild, with_test_phase = {0[with_test_phase]}, base_docker_image = {0[base_docker_image]}, use_flags = {0[use_flags]}).{1} == \'{2}\''.format(kwargs, prop, test[prop])

            return case

        def gen_run_case(test):
            kwargs = {
                'base_docker_image': test['base_docker_image'],
                'with_test_phase': test['with_test_phase'],
            }
            kwargs.setdefault('use_flags', test.get('use_flags', []))

            def case(self):
                self.test = tests.Test(
                    self.mocked_ebuild,
                    **kwargs
                )

                self.mock_docker()

                self.test.run()

                self.mocked_docker.pull.assert_called_once()

            case.__name__ = 'test_run_' + str(test['uuid'])
            case.__doc__ = 'test.Test(mocked_ebuild, with_test_phase = {0[with_test_phase]}, base_docker_image = {0[base_docker_image]}, use_flags = {0[use_flags]}).run()'.format(kwargs)

            return case

        for test in copy.deepcopy(TESTS['test']):
            _ = gen_constructor_case(test)
            logger.info('adding %s', _.__name__)
            setattr(cls, _.__name__, _)

            for prop in ( 'commands', 'environment', 'name', ):
                _ = gen_property_case(test, prop)
                logger.info('adding %s', _.__name__)
                setattr(cls, _.__name__, _)

            _ = gen_run_case(test)
            logger.info('adding %s', _.__name__)
            setattr(cls, _.__name__, _)


class TestUnitTest(BaseEtestTest, metaclass = BaseTestMetaTest):
    mocks_mask = set()
    mocks = set()

    def setUp(self):
        super().setUp()

        self.mocked_ebuild = unittest.mock.MagicMock()

    mocks.add('docker')

    @test_helpers.mock('docker')
    def mock_docker(self):
        self._patch('docker')


class TestsUnitTest(BaseEtestTest):
    mocks_mask = set()
    mocks = set()

    def setUp(self):
        super().setUp()

        self.mocked_directory = os.path.join(FIXTURES_DIRECTORY, 'overlay')

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(self.mocked_directory)

        self.mock_overlay()
        type(self.mocked_overlay_overlay).directory = unittest.mock.PropertyMock(return_value = self.mocked_directory)

        ebuilds = []

        self.test_calls = []

        for ebuild in copy.deepcopy(EBUILDS['all']):
            mocked_ebuild = unittest.mock.MagicMock()
            type(mocked_ebuild).use_flags = unittest.mock.PropertyMock(return_value = ebuild['use_flags'])
            type(mocked_ebuild).cpv = unittest.mock.PropertyMock(return_value = ebuild['cpv'])
            ebuilds.append(mocked_ebuild)

            for use_flag_set in ebuild['use_flag_sets']:
                self.test_calls.append(unittest.mock.call(mocked_ebuild, use_flags = use_flag_set, with_test_phase = False))
                self.test_calls.append(unittest.mock.call(mocked_ebuild, use_flags = use_flag_set, with_test_phase = True))

        type(self.mocked_overlay_overlay).ebuilds = unittest.mock.PropertyMock(return_value = ebuilds)

        self._patch('Test')

    mocks.add('overlay')

    @test_helpers.mock('overlay')
    def mock_overlay(self):
        self._patch('overlay')

        self.mocked_overlay_overlay = unittest.mock.MagicMock()
        self.mocked_overlay.Overlay.return_value = self.mocked_overlay_overlay

    def test_tests(self):
        '''tests.Tests()'''

        self.tests = tests.Tests()

        self.assertEqual(self.tests.ebuild_selector, [])
        self.assertEqual(len(list(self.tests)), len(self.test_calls))
        self.assertEqual(self.mocked_Test.mock_calls, self.test_calls)

    def test_tests_with_filter_with_version(self):
        '''tests.Tests(('etest-9999.ebuild',))'''

        self.tests = tests.Tests(('etest-9999.ebuild',))

        self.assertEqual(self.tests.ebuild_selector, ['etest-9999', ])
        self.assertEqual(len(list(self.tests)), 2)

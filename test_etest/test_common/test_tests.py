# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import datetime
import logging
import unittest
import unittest.mock

from test_etest import test_helpers
from test_etest.test_common import BaseEtestTest
from test_etest.test_fixtures.test_tests import TESTS

from etest.tests import Test

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
                self.test = Test(
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

                self.test = Test(
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
                self.test = Test(
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


class BaseTestTest(BaseEtestTest):
    mocks_mask = set()
    mocks = set()

    def setUp(self):
        super().setUp()

        self.mocked_ebuild = unittest.mock.MagicMock()

    mocks.add('docker')

    @test_helpers.mock('docker')
    def mock_docker(self):
        self._patch('docker')


class BaseTestsTest(BaseEtestTest):
    mocks_mask = set()
    mocks = set()

    def setUp(self):
        super().setUp()

        self.mock_overlay()

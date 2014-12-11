# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import logging
import os
import unittest
import unittest.mock

from test_etest.test_common import BaseEtestTest
from test_etest.test_fixtures import FIXTURES_DIRECTORY
from test_etest.test_fixtures.test_ebuilds import EBUILDS

from etest.ebuild import Ebuild

logger = logging.getLogger(__name__)


class BaseEbuildMetaTest(type):
    def __init__(cls, name, bases, dct):
        super(BaseEbuildMetaTest, cls).__init__(name, bases, dct)

        def gen_constructor_case(ebuild):
            def case(self):
                self.ebuild = Ebuild(
                    path = ebuild['path'],
                    overlay = self.mocked_overlay,
                )

                self.assertEqual(self.ebuild.path, ebuild['path'])
                self.assertEqual(self.ebuild.overlay, self.mocked_overlay)

            case.__name__ = 'test_constructor_' + str(ebuild['uuid'])
            case.__doc__ = 'ebuild.Ebuild(path = \'{0[path]}\', overlay = mocked_overlay)'.format(ebuild)

            return case

        def gen_property_case(ebuild, prop):
            def case(self):
                self.ebuild = Ebuild(
                    path = ebuild['path'],
                    overlay = self.mocked_overlay,
                )

                self.ebuild.parse = unittest.mock.MagicMock(return_value = ebuild['symbols'])

                self.assertEqual(getattr(self.ebuild, prop), ebuild[prop])

            case.__name__ = 'test_property_' + prop + '_' + str(ebuild['uuid'])
            case.__doc__ = 'ebuild.Ebuild(path = \'{0[path]}\', overlay = mocked_overlay).{1} == \'{2}\''.format(ebuild, prop, ebuild[prop])

            return case

        for ebuild in copy.deepcopy(EBUILDS['all']):
            _ = gen_constructor_case(ebuild)
            logger.info('adding %s', _.__name__)
            setattr(cls, _.__name__, _)

            for prop in ( 'compat', 'cpv', 'name', 'use_flags', 'version', 'restrictions', ):
                _ = gen_property_case(ebuild, prop)
                logger.info('adding %s', _.__name__)
                setattr(cls, _.__name__, _)


class EbuildUnitTest(BaseEtestTest, metaclass = BaseEbuildMetaTest):
    mocks_mask = set().union(BaseEtestTest.mocks_mask)
    mocks = set().union(BaseEtestTest.mocks)

    def setUp(self):
        super().setUp()

        self.mocked_overlay = unittest.mock.MagicMock()
        type(self.mocked_overlay).directory = unittest.mock.PropertyMock(return_value = os.path.join(FIXTURES_DIRECTORY, 'overlay'))

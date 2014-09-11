# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import unittest

from test_etest.test_fixtures.test_helpers import BASH_TEXTS

from etest.parsers.bash import BashParser, BashSyntaxError

logger = logging.getLogger(__name__)


class TestBashParser(unittest.TestCase):
    def setUp(self):
        self.texts = BASH_TEXTS
        self.parser = BashParser()
        self.parser.build()

    def test_correct(self):
        '''helpers.bash_to_dict()—correct parse'''

        for text in self.texts['correct']:
            self.assertEqual(text['dictionary'], self.parser.parser.parse(text['bash']))

    def test_incorrect(self):
        '''helpers.bash_to_dict()—incorrect parse'''

        for text in self.texts['incorrect']:
            self.assertRaises(BashSyntaxError, self.parser.parser.parse, text['bash'])

# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import unittest

from test_etest.test_fixtures.test_bash import BASH_TEXTS

from etest.lexers.bash import BashLexer, BashSyntaxError
from etest.parsers.bash import BashParser

logger = logging.getLogger(__name__)


class TestBashParser(unittest.TestCase):
    def setUp(self):
        self.texts = BASH_TEXTS
        self.lexer = BashLexer()
        self.parser = BashParser()

    def test_correct(self):
        '''parsers.bash—correct parse'''

        for text in self.texts['correct']:
            logger.info('name: %s', text['name'])

            self.lexer.build()
            self.parser.build()

            self.parser.parser.parse(
                input = text['bash'],
                lexer = self.lexer.lexer,
            )

            self.assertEqual(text['dictionary'], self.parser.symbols)

    def test_incorrect(self):
        '''parsers.bash—incorrect parse'''

        for text in self.texts['incorrect']:
            logger.info('name: %s', text['name'])

            self.lexer.build()
            self.parser.build()

            self.assertRaises(BashSyntaxError, self.parser.parser.parse, input = text['bash'], lexer = self.lexer.lexer)

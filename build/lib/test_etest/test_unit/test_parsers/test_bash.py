# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import logging
import os
import unittest

from test_etest.test_fixtures.test_scripts import SCRIPTS

from etest.lexers.bash import BashLexer, BashSyntaxError
from etest.parsers.bash import BashParser

logger = logging.getLogger(__name__)


class BaseParserMetaTest(type):
    def __init__(cls, name, bases, dct):
        super(BaseParserMetaTest, cls).__init__(name, bases, dct)

        def gen_script_case(script):
            def case(self):
                self.lexer = BashLexer()
                self.lexer.build()

                self.parser = BashParser()
                self.parser.build(
                    debug = 1,
                    debugfile = os.path.join(os.path.dirname(__file__), 'parser.out'),
                    debuglog = None,
                )

                if 'correct' in script:
                    logger.debug('script[text]: %r', script['text'])

                    self.parser.parser.parse(
                        debug = logger,
                        input = script['text'],
                        lexer = self.lexer.lexer,
                    )

                    self.assertEqual(script['symbols'], self.parser.symbols)
                else:
                    self.assertRaises(BashSyntaxError, self.parser.parser.parse, input = script['text'], lexer = self.lexer.lexer)

            case.__name__ = 'test_' + script['uuid']
            case.__doc__ = 'parsers.bash—{0[uuid]}—{0[description]}'.format(script)

            return case

        for script in copy.deepcopy(SCRIPTS['bash']):
            _ = gen_script_case(script)
            logger.info('adding %s', _.__name__)
            setattr(cls, _.__name__, _)


class BashParserUnitTest(unittest.TestCase, metaclass = BaseParserMetaTest):
    pass

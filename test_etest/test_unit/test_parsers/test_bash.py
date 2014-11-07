# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import logging
import os
import unittest

from test_etest.test_fixtures.test_bash import BASH_SCRIPTS

from etest.lexers.bash import BashLexer, BashSyntaxError
from etest.parsers.bash import BashParser

logger = logging.getLogger(__name__)


class TestBaseParserMeta(type):
    def __init__(cls, name, bases, dct):
        super(TestBaseParserMeta, cls).__init__(name, bases, dct)

        def gen_script_case(script, correct):
            def case(self):
                self.lexer = BashLexer()
                self.lexer.build()

                self.parser = BashParser()
                self.parser.build(
                    debug = 1,
                    debugfile = os.path.join(os.path.dirname(__file__), 'parser.out'),
                    debuglog = None,
                )

                if correct:
                    self.parser.parser.parse(
                        debug = logger,
                        input = script['bash'],
                        lexer = self.lexer.lexer,
                    )
                else:
                    self.assertRaises(BashSyntaxError, self.parser.parser.parse, input = script['bash'], lexer = self.lexer.lexer)

            case.__name__ = 'test_' + script['name']
            case.__doc__ = 'parsers.bash—{0[name]}'.format(script)

            if correct:
                case.__doc__ += '—correct'
            else:
                case.__doc__ += '—incorrect'

            return case

        for script in copy.deepcopy(BASH_SCRIPTS['correct']):
            logger.debug('adding %s to %s', script['name'], cls)

            setattr(cls, 'test_' + script['name'], gen_script_case(script, True))

        for script in copy.deepcopy(BASH_SCRIPTS['incorrect']):
            logger.debug('adding %s to %s', script['name'], cls)

            setattr(cls, 'test_' + script['name'], gen_script_case(script, False))


class TestBashParser(unittest.TestCase, metaclass = TestBaseParserMeta):
    pass

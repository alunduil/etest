"""Bash Parser Tests."""
import copy
import logging
import os
import unittest
from typing import Any, Callable, Dict, Mapping, Tuple, TypeVar

from etest.lexers.bash import BashLexer, BashSyntaxError
from etest.parsers.bash import BashParser
from etest_test.fixtures_test.scripts_test import SCRIPTS

logger = logging.getLogger(__name__)

TestCase = TypeVar("TestCase", bound=unittest.TestCase)


class BaseParserMetaTest(type):
    """Bash Parser Metatest."""

    def __init__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> None:
        """Construct a Bash Parser Meta Test."""
        super(BaseParserMetaTest, cls).__init__(name, bases, dct)

        def gen_script_case(
            script: Mapping[str, Any],
        ) -> Callable[[TestCase], None]:
            def case(self: TestCase) -> None:
                lexer = BashLexer()
                lexer.build()

                parser = BashParser()
                parser.build(
                    debug=1,
                    debugfile=os.path.join(os.path.dirname(__file__), "parser.out"),
                    debuglog=None,
                )

                assert parser.parser is not None  # nosec

                if "correct" in script:
                    logger.debug("script[text]: %r", script["text"])

                    assert parser is not None  # nosec
                    assert parser.parser is not None  # nosec

                    parser.parser.parse(
                        debug=logger,
                        input=script["text"],
                        lexer=lexer.lexer,
                    )

                    self.assertEqual(script["symbols"], parser.symbols)
                else:
                    with self.assertRaises(BashSyntaxError):
                        parser.parser.parse(input=script["text"], lexer=lexer.lexer)

            case.__name__ = f"test_{script['uuid']}"
            case.__doc__ = f"parsers.bash—{script['uuid']}—{script['description']}"

            return case

        for script in copy.deepcopy(SCRIPTS["bash"]):
            _ = gen_script_case(script)
            logger.info("adding %s", _.__name__)
            setattr(cls, _.__name__, _)


class BashParserUnitTest(unittest.TestCase, metaclass=BaseParserMetaTest):
    """Unit tests for Bash Parser."""

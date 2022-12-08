"""Bash Parser Tests."""
import logging

import pytest
import pytest_golden

import etest.lexers.bash as _lexer
import etest.parsers.bash as sut

_LOGGER = logging.getLogger(__name__)


@pytest.mark.golden_test("bash_test_fixtures/correct_*.yaml")  # type: ignore[misc]
def test_golden_bash_correct_parses(
    lexer: _lexer.BashLexer, golden: pytest_golden.plugin.GoldenTestFixture
) -> None:
    """Test golden corrects in BashParser."""
    parser = sut.BashParser()
    parser.build(debug=True, debuglog=_LOGGER)

    assert parser.parser is not None  # nosec

    parser.parser.parse(input=golden["text"], lexer=lexer.lexer, debug=_LOGGER)

    assert parser.symbols == golden.out["symbols"]  # nosec


@pytest.mark.golden_test("bash_test_fixtures/error_*.yaml")  # type: ignore[misc]
def test_golden_bash_error_parses(
    lexer: _lexer.BashLexer, golden: pytest_golden.plugin.GoldenTestFixture
) -> None:
    """Test golden errors in BashParser."""
    parser = sut.BashParser()
    parser.build(debug=True, debuglog=_LOGGER)

    assert parser.parser is not None  # nosec

    with pytest.raises(sut.BashSyntaxError):
        parser.parser.parse(input=golden["text"], lexer=lexer.lexer, debug=_LOGGER)

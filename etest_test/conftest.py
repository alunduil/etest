"""Fixtures for pytest."""

import pytest

import etest.lexers.bash as _lexer


@pytest.fixture  # type: ignore[misc]
def lexer() -> _lexer.BashLexer:
    """Fixture for the BASH lexer."""
    result = _lexer.BashLexer()
    result.build()
    return result

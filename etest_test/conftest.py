"""Fixtures for pytest."""

import os
import pathlib
import shutil

import pytest

import etest.lexers.bash as _lexer
import etest_test.overlay as _overlay


@pytest.fixture  # type: ignore[misc]
def lexer() -> _lexer.BashLexer:
    """Fixture for the BASH lexer."""
    result = _lexer.BashLexer()
    result.build()
    return result


@pytest.fixture  # type: ignore[misc]
def overlay(tmp_path: pathlib.Path) -> pathlib.Path:
    """Fixture for use as an overlay directory."""
    shutil.copytree(
        _overlay.PATH,
        tmp_path,
        ignore=shutil.ignore_patterns("__init__.py", "__pycache__"),
        dirs_exist_ok=True,
    )
    return tmp_path

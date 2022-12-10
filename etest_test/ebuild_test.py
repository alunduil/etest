"""Ebuild Tests."""
import logging
import unittest
import unittest.mock

import pytest
import pytest_golden

import etest.ebuild as sut
import etest.overlay as _overlay

_LOGGER = logging.getLogger(__name__)


@pytest.mark.golden_test("ebuild_test_fixtures/*.yaml")  # type: ignore[misc]
def test_golden_ebuilds(
    overlay: _overlay.Overlay, golden: pytest_golden.plugin.GoldenTestFixture
) -> None:
    """Test golden ebuilds."""
    result = sut.Ebuild(path=golden["path"], overlay=overlay)
    with unittest.mock.patch.object(
        result, "parse", return_value=golden["symbols"]
    ) as mock_parse:
        assert result.compat == golden.out["properties"]["compat"]  # nosec
        assert result.cpv == golden.out["properties"]["cpv"]  # nosec
        assert result.name == golden.out["properties"]["name"]  # nosec
        assert result.use_flags == golden.out["properties"]["use_flags"]  # nosec
        assert result.version == golden.out["properties"]["version"]  # nosec
        assert result.restrictions == golden.out["properties"]["restrictions"]  # nosec
        mock_parse.assert_called()

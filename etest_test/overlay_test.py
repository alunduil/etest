"""Overlay Test."""
import pathlib

import pytest

import etest.overlay as sut


class TestRoot:
    """Test root detectrion of overlay."""

    def test_empty_directory(self, tmp_path: pathlib.Path) -> None:
        """Test detection of root for a completely empty overlay."""
        with pytest.raises(sut.InvalidOverlayError):
            sut.root(path=tmp_path)

    def test_minimal_overlay(self, empty_overlay: pathlib.Path) -> None:
        """Test detection of root for a minimally empty overlay."""
        assert sut.root(empty_overlay) == empty_overlay  # nosec

    def test_overlay(self, overlay: pathlib.Path) -> None:
        """Test detection of root for a non-empty overlay."""
        assert sut.root(overlay) == overlay  # nosec


class TestEbuilds:
    """Test Ebuild listing of overlays."""

    def test_minimal_overlay(self, empty_overlay: pathlib.Path) -> None:
        """Test listing of ebuilds in an empty overaly."""
        assert len(list(sut.ebuilds(empty_overlay))) == 0  # nosec

    def test_overlay(self, overlay: pathlib.Path) -> None:
        """Test listing of ebuilds in an non-empty overlay."""
        assert len(list(sut.ebuilds(overlay))) == 1  # nosec

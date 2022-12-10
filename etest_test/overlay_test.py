"""Overlay Test."""
import pathlib

import pytest

import etest.overlay as sut


class TestRoot:
    """Test root discovery."""

    def test_invalid(self, tmp_path: pathlib.Path) -> None:
        """Test root discovery a non-overlay."""
        with pytest.raises(sut.InvalidOverlayError):
            sut.root(tmp_path)

    def test_empty(self, tmp_path: pathlib.Path) -> None:
        """Test root discovery of an empty overlay."""
        (tmp_path / "metadata" / "layout.conf").write_text("masters = gentoo")
        assert sut.root(tmp_path) == tmp_path  # nosec

    def test_nonempty(self, overlay: pathlib.Path) -> None:
        """Test root discovery of a non-empty overlay."""
        assert sut.root(overlay) == overlay  # nosec


class TestEbuilds:
    """Test listing ebuilds."""

    def test_invalid(self, tmp_path: pathlib.Path) -> None:
        """Test listing of a non-overlay."""
        with pytest.raises(sut.InvalidOverlayError):
            sut.ebuilds(tmp_path)

    def test_empty(self, tmp_path: pathlib.Path) -> None:
        """Test listing of an empty overlay."""
        (tmp_path / "metadata" / "layout.conf").write_text("masters = gentoo")
        assert len(list(sut.ebuilds(tmp_path))) == 0  # nosec

    def test_nonempty(self, overlay: pathlib.Path) -> None:
        """Test listing of a non-empty overlay."""
        assert len(list(sut.ebuilds(overlay))) > 0  # nosec

"""Overlay Test."""
import functools
import logging
import os
import pathlib
import tempfile
import unittest.mock

import etest.overlay as sut
from etest_test.fixtures_test import FIXTURES_DIRECTORY

logger = logging.getLogger(__name__)


@unittest.mock.patch.object(sut, "ebuild")
class BaseOverlayTest(unittest.TestCase):
    """Overlay test."""

    def setUp(self) -> None:
        """Set up test cases."""
        super().setUp()

        self.overlay = sut.Overlay()


class InvalidOverlayUnitTest(BaseOverlayTest):
    """Invalid overlays."""

    def test_invalid_overlay(self) -> None:
        """overlay.Overlay()—invalid overlay."""
        self.assertRaises(sut.InvalidOverlayError, getattr, self.overlay, "directory")


class ValidEmptyOverlayUnitTest(BaseOverlayTest):
    """Empty overlays."""

    def setUp(self) -> None:
        """Set up test cases."""
        super().setUp()

        self.mocked_directory = tempfile.mkdtemp()
        self.addCleanup(os.rmdir, self.mocked_directory)

        _ = os.path.join(self.mocked_directory, "metadata")
        os.mkdir(_)
        self.addCleanup(os.rmdir, _)

        layout_conf = pathlib.Path(self.mocked_directory) / "metadata" / "layout.conf"
        layout_conf.write_text("masters = gentoo")
        self.addCleanup(os.remove, layout_conf)

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(self.mocked_directory)

    def test_empty_overlay_discovery(self) -> None:
        """overlay.Overlay().directory—empty overlay."""
        self.assertEqual(self.overlay.directory, self.mocked_directory)

    def test_empty_overlay_ebuilds(self) -> None:
        """len(list(overlay.Overlay().ebuilds)) == 0—empty overlay."""
        self.assertEqual(0, len(list(self.overlay.ebuilds)))


class ValidNonEmptyOverlayUnitTest(BaseOverlayTest):
    """Check Empty Overlays."""

    def setUp(self) -> None:
        """Set up test cases."""
        super().setUp()

        self.mocked_directory = os.path.join(FIXTURES_DIRECTORY, "overlay")

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(self.mocked_directory)

    def test_nonempty_overlay_discovery(self) -> None:
        """overlay.Overlay().directory—nonempty overlay."""
        self.assertEqual(self.overlay.directory, self.mocked_directory)

    def test_nonempty_overlay_ebuilds(self) -> None:
        """len(list(overlay.Overlay().ebuilds)) == 1—nonempty overlay."""
        self.assertEqual(1, len(list(self.overlay.ebuilds)))


class ValidNonEmptyOverlaySubdirectoryUnitTest(BaseOverlayTest):
    """Check Non-empty Overlay Subdirectory Tests."""

    def setUp(self) -> None:
        """Set up test cases."""
        super().setUp()

        self.mocked_overlay_directory = os.path.join(FIXTURES_DIRECTORY, "overlay")
        self.mocked_directory = os.path.join(
            self.mocked_overlay_directory, "app-portage", "etest"
        )

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(self.mocked_directory)

    def test_nonempty_overlay_discovery(self) -> None:
        """overlay.Overlay().directory—nonempty overlay,subdirectory."""
        self.assertEqual(self.overlay.directory, self.mocked_overlay_directory)

    def test_nonempty_overlay_ebuilds(self) -> None:
        """Number of ebuilds equals 1 for non-empty subdirectories."""
        self.assertEqual(1, len(list(self.overlay.ebuilds)))

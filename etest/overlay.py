"""Overlay."""
import functools
import logging
import os
from typing import Generator

from etest import ebuild

logger = logging.getLogger(__name__)


class Overlay:
    """A portage defined overlay."""

    @functools.cached_property
    def directory(self) -> str:
        """Directory containing overlay."""
        path = os.getcwd()

        while path != "/":
            if os.path.exists(os.path.join(path, "metadata", "layout.conf")):
                break

            path = os.path.dirname(path)
        else:
            raise InvalidOverlayError("not in a valid ebuild repository directory")

        return path

    @property
    def ebuilds(self) -> Generator[ebuild.Ebuild, None, None]:
        """Contained ebuilds in overlay."""
        for path, directories, files in os.walk(self.directory):
            if "files" in directories:
                directories.remove("files")

            for _ in files:
                if _.endswith(".ebuild"):
                    yield ebuild.Ebuild(
                        os.path.relpath(os.path.join(path, _), self.directory), self
                    )


class InvalidOverlayError(RuntimeError):
    """Overlay is invalid."""

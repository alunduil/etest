"""Overlay."""
import logging
import pathlib
import typing

import etest.ebuild as _ebuild

_LOGGER = logging.getLogger(__name__)


def root(path: pathlib.Path = pathlib.Path.cwd()) -> pathlib.Path:
    """Directory containing overlay."""
    if path.is_dir() and (path / "metadata" / "layout.conf").exists():
        return path
    for parent in path.parents:
        if (parent / "metadata" / "layout.conf").exists():
            return parent

    raise InvalidOverlayError(f"{path} not in a valid ebuild repository directory.")


def ebuilds(
    path: pathlib.Path = pathlib.Path.cwd(),
) -> typing.Generator[_ebuild.Ebuild, None, None]:
    """Contained ebuilds in overlay."""
    repository_path = root(path)
    yield from (
        _ebuild.Ebuild(
            path=str(p.relative_to(repository_path)), overlay=repository_path
        )
        for p in repository_path.rglob("*.ebuild")
    )


class InvalidOverlayError(RuntimeError):
    """Overlay is invalid."""

"""Overlay."""
import functools
import logging
import os
import pathlib
import typing

import etest.ebuild as _ebuild

_LOGGER = logging.getLogger(__name__)


class InvalidOverlayError(RuntimeError):
    """Overlay is invalid."""


@functools.lru_cache
def root(path: pathlib.Path = pathlib.Path(os.getcwd())) -> pathlib.Path:
    """Find root directory of ebuild repository containing path."""
    _LOGGER.info("searching for ebuild repository root containing %s.", path)

    result = path
    while result != result.root:
        if (result / "metadata" / "layout.conf").exists():
            break
        result = result.parent
    else:
        raise InvalidOverlayError(f"{path} is not in a valid ebuild repository.")

    return result


def ebuilds(
    path: pathlib.Path = root(),
) -> typing.Generator[_ebuild.Ebuild, None, None]:
    """Find all ebuilds in the overlay containing path."""
    yield from (
        _ebuild.Ebuild(ebuild, root(path)) for ebuild in root(path).rglob("*.ebuild")
    )

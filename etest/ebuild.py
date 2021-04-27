"""Ebuild."""
# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import logging
import os
import re
from typing import Any, Dict, List

from etest.lexers.bash import BashLexer, BashSyntaxError
from etest.parsers.bash import BashParser

logger = logging.getLogger(__name__)


class Ebuild(object):
    """Ebuild."""

    def __init__(self, path: str, overlay: Any) -> None:
        """Construct an ebuild."""
        self.path = path
        self.overlay = overlay

    @functools.cached_property
    def name(self) -> str:
        """Name of ebuild."""
        return os.path.dirname(self.path)

    @functools.cached_property
    def cpv(self) -> str:
        """Category package version."""
        return "=" + self.name + "-" + self.version

    @functools.cached_property
    def version(self) -> str:
        """Version of ebuild."""
        result = self.path.replace(".ebuild", "")
        result = re.sub(r".*?" + re.escape(self.name.split("/")[-1]) + "-", "", result)

        return result

    @functools.cached_property
    def compat(self) -> Dict[str, str]:
        """COMPAT for ebuild."""
        return {k.replace("_COMPAT", "").lower(): v for k, v in self.parse().items() if "_COMPAT" in k}

    @functools.cached_property
    def restrictions(self) -> List[str]:
        """Ebuild Restrictions."""
        return self.parse().get("RESTRICT", "").split()

    @functools.cached_property
    def use_flags(self) -> List[str]:
        """USE flags for ebuild."""
        return [re.sub(r"^[+-]", "", _) for _ in self.parse()["IUSE"].split()]

    @functools.lru_cache(1)
    def parse(self) -> Dict[str, str]:
        """Convert ebuild file into a dictionary, mapping variables to values.

        Parses the ebuild file and constructs a dictionary that maps the
        variables to their values.

        Returns
        -------
        Dictionary whose keys are variables in the associated ebuild.
        """
        parser = BashParser()
        parser.build()

        assert parser.parser is not None

        lexer = BashLexer()
        lexer.build()

        ebuild_filename = os.path.join(self.overlay.directory, self.path)

        with open(ebuild_filename, "r") as fh:
            try:
                parser.parser.parse(
                    input=fh.read(),
                    lexer=lexer.lexer,
                )
            except BashSyntaxError as error:
                error.message = ebuild_filename + "\n" + error.message
                raise

        return parser.symbols

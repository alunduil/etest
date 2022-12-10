"""Ebuild."""
import dataclasses
import logging
import pathlib
import re
import typing

from etest.lexers.bash import BashLexer, BashSyntaxError
from etest.parsers.bash import BashParser

_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class Ebuild:  # pylint: disable=R0902
    """Ebuild."""

    overlay: pathlib.Path
    path: pathlib.Path
    symbols: typing.Dict[str, typing.Any]
    name: str = dataclasses.field(init=False)
    version: str = dataclasses.field(init=False)
    cpv: str = dataclasses.field(init=False)
    compat: typing.Dict[str, typing.Any] = dataclasses.field(init=False)
    restrictions: typing.List[str] = dataclasses.field(init=False)
    use_flags: typing.List[str] = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        """Post initialisation of Ebuild properties."""
        category = str(self.path.parent.parent.name)
        self.name = f"{category}/" + re.sub(r"-\d.*", "", self.path.stem, 1)
        self.version = re.sub(r".*-(?=\d)", "", self.path.stem, 1)
        self.cpv = f"={category}/{self.path.stem}"
        self.compat = {
            key.replace("_COMPAT", "").lower(): value
            for key, value in self.symbols.items()
            if "_COMPAT" in key
        }
        self.restrictions = self.symbols.get("RESTRICT", "").split()
        self.use_flags = [re.sub(r"^[+-]", "", i) for i in self.symbols["IUSE"].split()]

    @classmethod
    def from_file(cls, path: pathlib.Path, overlay: pathlib.Path) -> "Ebuild":
        """Convert ebuild file into a dictionary, mapping variables to values.

        Parses the ebuild file and constructs a dictionary that maps the
        variables to their values.

        Returns
        -------
        Dictionary whose keys are variables in the associated ebuild.
        """
        _LOGGER.info("reading ebuild from %s", path)

        parser = BashParser()
        parser.build()

        assert parser.parser is not None  # nosec

        lexer = BashLexer()
        lexer.build()

        try:
            parser.parser.parse(
                input=path.read_text(), lexer=lexer.lexer, debug=_LOGGER, tracking=True
            )
        except BashSyntaxError as error:
            error.message = f"{path}: {error.message}"
            raise

        return cls(
            overlay=overlay,
            path=path.relative_to(overlay),
            symbols=parser.symbols,
        )

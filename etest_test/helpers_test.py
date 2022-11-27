"""Helper functions for testing."""
import importlib
import itertools
import logging
import os
import sys

logger = logging.getLogger(__name__)


def import_directory(
    module_basename: str, directory: str, update_path: bool = False
) -> None:
    """Load all modules in a given directory recursively.

    All python modules in the given directory will be imported.

    Parameters
    ----------
    :``module_basename``: Module name prefix for loaded modules.
    :``directory``:       Directory to recursively load python modules from.
    :``update_path``:     If True, the system path for modules is updated to
                          include ``directory``; otherwise, it is left alone.
    """
    if update_path:
        update_path = bool(sys.path.count(directory))
        sys.path.append(directory)

    logger.info("loading submodules of %s", module_basename)
    logger.info("loading modules from %s", directory)

    filenames = itertools.chain(
        *[
            [os.path.join(_[0], filename) for filename in _[2]]
            for _ in os.walk(directory)
            if len(_[2])
        ]
    )

    module_names = []
    for filename in filenames:
        if filename.endswith(".py"):
            name = filename

            name = name.replace(directory + "/", "")
            name = name.replace("__init__.py", "")
            name = name.replace(".py", "")
            name = name.replace("/", ".")
            name = name.strip(".")

            if not name:
                continue

            name = module_basename + "." + name

            known_symbols = set()
            name = ".".join(
                [
                    _
                    for _ in name.split(".")
                    if _ not in known_symbols and not known_symbols.add(_)  # type: ignore[func-returns-value]
                ]
            )

            if name:
                module_names.append(name)

    logger.debug("modules found: %s", list(module_names))

    for module_name in module_names:
        logger.info("loading module %s", module_name)

        try:
            importlib.import_module(module_name)
        except ImportError:
            logger.exception("failed loading %s", module_name)
        else:
            logger.info("successfully loaded %s", module_name)

    if update_path:
        sys.path.remove(directory)

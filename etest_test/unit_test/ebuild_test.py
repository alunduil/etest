"""Ebuild Tests."""
import copy
import logging
import os
import unittest
import unittest.mock
from typing import Any, Callable, Dict, Tuple

from etest.ebuild import Ebuild
from etest_test.fixtures_test import FIXTURES_DIRECTORY
from etest_test.fixtures_test.ebuilds_test import EBUILDS

logger = logging.getLogger(__name__)


class BaseEbuildMetaTest(type):
    """Base Ebuild Metatest."""

    def __init__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> None:
        """Construct a base Ebuild meta test."""
        super(BaseEbuildMetaTest, cls).__init__(name, bases, dct)

        def gen_constructor_case(
            ebuild: Dict[str, Any]
        ) -> Callable[["EbuildUnitTest"], None]:
            def case(self: "EbuildUnitTest") -> None:
                result = Ebuild(
                    path=ebuild["path"],
                    overlay=self.mocked_overlay,
                )

                self.assertEqual(result.path, ebuild["path"])
                self.assertEqual(result.overlay, self.mocked_overlay)

            case.__name__ = "test_constructor_" + str(ebuild["uuid"])
            case.__doc__ = (
                f"ebuild.Ebuild(path = '{ebuild['path']}', overlay = mocked_overlay)"
            )

            return case

        def gen_property_case(
            ebuild: Dict[str, Any], prop: str
        ) -> Callable[["EbuildUnitTest"], None]:
            def case(self: "EbuildUnitTest") -> None:
                result = Ebuild(
                    path=ebuild["path"],
                    overlay=self.mocked_overlay,
                )

                result.parse = unittest.mock.MagicMock(return_value=ebuild["symbols"])

                self.assertEqual(getattr(result, prop), ebuild[prop])

            case.__name__ = "test_property_" + prop + "_" + str(ebuild["uuid"])
            case.__doc__ = f"ebuild.Ebuild(path = '{ebuild['path']}', overlay = mocked_overlay).{prop} == '{ebuild[prop]}'"  # noqa: E501 # pylint: disable=C0301

            return case

        for ebuild in copy.deepcopy(EBUILDS["all"]):
            _ = gen_constructor_case(ebuild)
            logger.info("adding %s", _.__name__)
            setattr(cls, _.__name__, _)

            for prop in (
                "compat",
                "cpv",
                "name",
                "use_flags",
                "version",
                "restrictions",
            ):
                _ = gen_property_case(ebuild, prop)
                logger.info("adding %s", _.__name__)
                setattr(cls, _.__name__, _)


class EbuildUnitTest(unittest.TestCase, metaclass=BaseEbuildMetaTest):
    """Ebuild Unit Test."""

    def setUp(self) -> None:
        """Set up test cases."""
        super().setUp()

        self.mocked_overlay = unittest.mock.MagicMock()
        type(self.mocked_overlay).directory = unittest.mock.PropertyMock(
            return_value=os.path.join(FIXTURES_DIRECTORY, "overlay"),
        )

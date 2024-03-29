"""Meta testing framework.

I'm not quite sure what this is anymore so we should update this
documentation as we discover its purpose again.
"""
import copy
import datetime
import functools
import logging
import os
import unittest
import unittest.mock
from typing import Any, Callable, Dict, Tuple

import etest.tests as sut
import etest_test.overlay as _overlay
from etest_test.fixtures_test.ebuilds_test import EBUILDS
from etest_test.fixtures_test.tests_test import TESTS

logger = logging.getLogger(__name__)


class BaseTestMetaTest(type):
    """Base Test for Meta Tests."""

    def __init__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> None:
        """Construct a BaseTestMetaTest."""
        super(BaseTestMetaTest, cls).__init__(name, bases, dct)

        def gen_constructor_case(
            test: Dict[str, Any]
        ) -> Callable[["TestUnitTest"], None]:
            kwargs = {
                "base_docker_image": test["base_docker_image"],
                "with_test_phase": test["with_test_phase"],
            }
            kwargs.setdefault("use_flags", test.get("use_flags", []))

            def case(self: "TestUnitTest") -> None:
                result = sut.Test(self.mocked_ebuild, **kwargs)

                self.assertEqual(result.ebuild, self.mocked_ebuild)
                self.assertEqual(result.with_test_phase, test["with_test_phase"])
                self.assertEqual(result.use_flags, test["use_flags"])
                self.assertFalse(result.failed)
                self.assertIsNone(result.failed_command)
                self.assertEqual(result.time, datetime.timedelta(0))
                self.assertEqual(result.output, "")
                self.assertEqual(result.base_docker_image, test["base_docker_image"])

            case.__name__ = "test_constructor_" + str(test["uuid"])
            case.__doc__ = f"test.Test(mocked_ebuild, with_test_phase = {kwargs['with_test_phase']}, base_docker_image = {kwargs['base_docker_image']}, use_flags = {kwargs['use_flags']})"  # noqa: E501 # pylint: disable=C0301

            return case

        def gen_property_case(
            test: Dict[str, Any], prop: str
        ) -> Callable[["TestUnitTest"], None]:
            kwargs = {
                "base_docker_image": test["base_docker_image"],
                "with_test_phase": test["with_test_phase"],
            }
            kwargs.setdefault("use_flags", test.get("use_flags", []))

            def case(self: "TestUnitTest") -> None:
                type(self.mocked_ebuild).compat = unittest.mock.PropertyMock(
                    return_value=test["ebuild"]["compat"]
                )
                type(self.mocked_ebuild).cpv = unittest.mock.PropertyMock(
                    return_value=test["ebuild"]["cpv"]
                )
                type(self.mocked_ebuild).name = unittest.mock.PropertyMock(
                    return_value=test["ebuild"]["name"]
                )

                result = sut.Test(self.mocked_ebuild, **kwargs)

                print(f"test: {test}")
                print(f"prop: {prop}")
                self.assertEqual(getattr(result, prop), test[prop])

            case.__name__ = "test_property_" + prop + "_" + str(test["uuid"])
            case.__doc__ = f"test.Test(mocked_ebuild, with_test_phase = {kwargs['with_test_phase']}, base_docker_image = {kwargs['base_docker_image']}, use_flags = {kwargs['use_flags']}).{prop} == '{test[prop]}'"  # noqa: E501 # pylint: disable=C0301

            return case

        def gen_run_case(test: Dict[str, Any]) -> Callable[["TestUnitTest"], None]:
            kwargs = {
                "base_docker_image": test["base_docker_image"],
                "with_test_phase": test["with_test_phase"],
            }
            kwargs.setdefault("use_flags", test.get("use_flags", []))

            def case(self: "TestUnitTest") -> None:
                result = sut.Test(self.mocked_ebuild, **kwargs)

                with unittest.mock.patch.object(sut, "docker") as mocked_docker:
                    result.run()
                    mocked_docker.pull.assert_called_once()

            case.__name__ = "test_run_" + str(test["uuid"])
            case.__doc__ = f"test.Test(mocked_ebuild, with_test_phase = {kwargs['with_test_phase']}, base_docker_image = {kwargs['base_docker_image']}, use_flags = {kwargs['use_flags']}).run()"  # noqa: E501 # pylint: disable=C0301

            return case

        for test in copy.deepcopy(TESTS["test"]):
            _ = gen_constructor_case(test)
            logger.info("adding %s", _.__name__)
            setattr(cls, _.__name__, _)

            for prop in ("commands", "environment", "name"):
                _ = gen_property_case(test, prop)
                logger.info("adding %s", _.__name__)
                setattr(cls, _.__name__, _)

            _ = gen_run_case(test)
            logger.info("adding %s", _.__name__)
            setattr(cls, _.__name__, _)


class TestUnitTest(unittest.TestCase, metaclass=BaseTestMetaTest):
    """Tests for Test Case."""

    def setUp(self) -> None:
        """Set Up Test Case."""
        super().setUp()

        self.mocked_ebuild = unittest.mock.MagicMock()


class TestsUnitTest(unittest.TestCase):
    """Tests for Tests Container."""

    def setUp(self) -> None:
        """Set Up Test Case."""
        super().setUp()

        self.mocked_directory = _overlay.PATH

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(self.mocked_directory)

        patcher = unittest.mock.patch.object(sut, "overlay")
        self.mocked_overlay = patcher.start()
        self.addCleanup(patcher.stop)

        ebuilds = []

        self.test_calls = []

        for ebuild in copy.deepcopy(EBUILDS["all"]):
            mocked_ebuild = unittest.mock.MagicMock()
            type(mocked_ebuild).use_flags = unittest.mock.PropertyMock(
                return_value=ebuild["use_flags"]
            )
            type(mocked_ebuild).cpv = unittest.mock.PropertyMock(
                return_value=ebuild["cpv"]
            )
            ebuilds.append(mocked_ebuild)

            for use_flag_set in ebuild["use_flag_sets"]:
                self.test_calls.append(
                    unittest.mock.call(
                        mocked_ebuild, use_flags=use_flag_set, with_test_phase=False
                    )
                )
                self.test_calls.append(
                    unittest.mock.call(
                        mocked_ebuild, use_flags=use_flag_set, with_test_phase=True
                    )
                )

        type(self.mocked_overlay).ebuilds = unittest.mock.MagicMock(
            return_value=ebuilds
        )

        patcher = unittest.mock.patch.object(sut, "Test")
        self.mocked_Test = patcher.start()  # pylint: disable=C0103
        self.addCleanup(patcher.stop)

    def test_tests(self) -> None:
        """tests.Tests()."""
        tests = sut.Tests()
        self.assertEqual(tests.ebuild_selector, [])
        self.assertEqual(len(list(tests)), len(self.test_calls))
        self.assertEqual(self.mocked_Test.mock_calls, self.test_calls)

    def test_tests_with_filter_with_version(self) -> None:
        """tests.Tests(('etest-9999.ebuild',))."""
        tests = sut.Tests(("etest-9999.ebuild",))
        self.assertEqual(tests.ebuild_selector, ["etest-9999"])
        self.assertEqual(len(list(tests)), 2)

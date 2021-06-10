"""app-portage/etest ebuild test."""
# pylint: disable=C0103
from etest_test.fixtures_test.ebuilds_test.eab5f11185a74264acb98eeb95b3238f import (
    _ as ebuild,
)
from etest_test.fixtures_test.tests_test import TESTS

_ = {
    "uuid": "27815bf0-5fa7-437f-a68b-ba9372139e9b",
    "ebuild": ebuild,
    "with_test_phase": False,
    "base_docker_image": "ebuildtest/etest:amd64",
    "use_flags": (),
    "name": "=app-portage_etest-9999[]",
    "commands": [
        [
            "bash",
            "-c",
            "echo app-portage/etest '-*'  >> /etc/portage/package.use/etest",
        ],
        [
            "bash",
            "-c",
            "echo app-portage/etest ~amd64 >> /etc/portage/package.accept_keywords/etest",
        ],
        [
            "bash",
            "-c",
            "emerge -q -f --autounmask-write =app-portage/etest-9999 >/dev/null 2>&1 || true",
        ],
        ["bash", "-c", "etc-update --automode -5 >/dev/null 2>&1"],
        ["emerge", "-q", "--backtrack=130", "=app-portage/etest-9999"],
    ],
    "environment": {
        "PYTHON_TARGETS": "python3_3 python3_4 python2_7",
    },
}

TESTS.setdefault("test", []).append(_)

"""app-portage/etest ebuild test."""
# pylint: disable=C0103
from etest_test.fixtures_test.ebuilds_test import EBUILDS

_ = {
    "uuid": "eab5f111-85a7-4264-acb98-eeb95b3238f",
    "path": "app-portage/etest/etest-9999.ebuild",
    "compat": {"python": ("python3_3", "python3_4")},
    "cpv": "=app-portage/etest-9999",
    "name": "app-portage/etest",
    "restrictions": [],
    "use_flags": ["test"],
    "version": "9999",
    "symbols": {
        "IUSE": "test",
        "PYTHON_COMPAT": ("python3_3", "python3_4"),
    },
    "use_flag_sets": ((),),
}

EBUILDS.setdefault("all", []).append(_)

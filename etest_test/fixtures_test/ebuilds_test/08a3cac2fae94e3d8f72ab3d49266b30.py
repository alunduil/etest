"""net-wireless/grimwepa."""
# pylint: disable=C0103
from etest_test.fixtures_test.ebuilds_test import EBUILDS

_ = {
    "uuid": "08a3cac2-fae9-4e3d-8f72-ab3d49266b30",
    "path": "net-wireless/grimwepa/grimwepa-1.10_p5-r100.ebuild",
    "compat": {},
    "cpv": "=net-wireless/grimwepa-1.10_p5-r100",
    "name": "net-wireless/grimwepa",
    "restrictions": [],
    "use_flags": ["wep", "extra"],
    "version": "1.10_p5-r100",
    "symbols": {
        "IUSE": "+wep +extra",
    },
    "use_flag_sets": (
        (),
        ("wep",),
        ("extra",),
        ("wep", "extra"),
    ),
}

EBUILDS.setdefault("all", []).append(_)

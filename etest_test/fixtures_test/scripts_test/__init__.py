"""Scripts Fixtures."""
import os
from typing import Any, Dict, List, Mapping

from etest_test import helpers_test

SCRIPTS: Dict[str, List[Mapping[str, Any]]] = {}

helpers_test.import_directory(__name__, os.path.dirname(__file__))

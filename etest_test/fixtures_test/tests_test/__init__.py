"""Fixture tests."""
import os
from typing import Any, Dict, List

from etest_test import helpers_test

TESTS: Dict[str, List[Dict[str, Any]]] = {}

helpers_test.import_directory(__name__, os.path.dirname(__file__))

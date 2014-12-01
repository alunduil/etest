# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import os
import re
import tempfile
import unittest

from test_etest.test_fixtures import FIXTURES_DIRECTORY


class BaseEtestTest(unittest.TestCase):
    @property
    def real_module(self):
        return re.sub(r'\.[^.]+', '', self.__module__.replace('test_', ''), 1)


class BaseEmptyOverlayTest(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.mocked_directory = tempfile.mkdtemp()
        self.addCleanup(os.rmdir, self.mocked_directory)

        _ = os.path.join(self.mocked_directory, 'profiles')
        os.mkdir(_)
        self.addCleanup(os.rmdir, _)

        _ = os.path.join(self.mocked_directory, 'profiles', 'repo_name')
        with open(_, 'w') as fh:
            fh.write('etest')
        self.addCleanup(os.remove, _)

        _ = os.path.join(self.mocked_directory, 'metadata')
        os.mkdir(_)
        self.addCleanup(os.rmdir, _)

        _ = os.path.join(self.mocked_directory, 'metadata', 'layout.conf')
        with open(_, 'w') as fh:
            fh.write('masters = gentoo')
        self.addCleanup(os.remove, _)

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(self.mocked_directory)


class BaseFixtureOverlayTest(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.mocked_directory = os.path.join(FIXTURES_DIRECTORY, 'overlay')

        self.addCleanup(functools.partial(os.chdir, os.getcwd()))
        os.chdir(self.mocked_directory)

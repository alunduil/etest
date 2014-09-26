# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import os
import tempfile
import unittest


class TestWithEmptyOverlay(unittest.TestCase):
    def setUp(self):
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

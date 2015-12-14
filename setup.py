# Copyright (C) 2015 etest project developers.
#
# See the COPYRIGHT file at the top-level directory of this distribution and at
# https://github.com/alunduil/etest/blob/master/COPYRIGHT
#
# etest is freely distributable under the terms of an MIT-style license.
# See LICENSE or http://www.opensource.org/licenses/mit-license.php.

import os
import sys

from codecs import open
from distutils.core import Command
from setuptools import find_packages
from setuptools import setup

with open(os.path.join('etest', 'information.py'), 'r', encoding = 'utf-8') as fh:
    exec(fh.read(), globals(), locals())

PARAMS = {}

PARAMS['name'] = NAME  # noqa (provided by exec)
PARAMS['version'] = VERSION  # noqa (provided by exec)
PARAMS['description'] = DESCRIPTION  # noqa (provided by exec)

with open('README.rst', 'r', encoding = 'utf-8') as fh:
    PARAMS['long_description'] = fh.read()

PARAMS['url'] = URL  # noqa (provided by exec)
PARAMS['author'] = AUTHOR  # noqa (provided by exec)
PARAMS['author_email'] = AUTHOR_EMAIL  # noqa (provided by exec)
PARAMS['license'] = LICENSE  # noqa (provided by exec)

PARAMS['classifiers'] = [
    'Development Status :: 3 - Alpha',
    # 'Development Status :: 4 - Beta',
    # 'Development Status :: 5 - Production/Stable',
    # 'Development Status :: 6 - Mature',
    # 'Development Status :: 7 - Inactive',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
    'Topic :: Utilities',
]

PARAMS['keywords'] = [
    'ebuild',
    'test',
    'gentoo',
    'portage',
    'emerge',
]

PARAMS['packages'] = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
PARAMS['package_data'] = {
    'etest.parsers': [ 'bash.p' ],
}

PARAMS['install_requires'] = [
    'click',
    'docker-py',
    'ply',
]

PARAMS['tests_require'] = [
    'coverage'
    'nose',
]


class test(Command):
    description = 'run all tests'

    user_options = [
        ( 'nosetests-arguments=', None, 'arguments for nosetests', ),
    ]

    def initialize_options(self):
        self.nosetests_arguments = None

    def finalize_options(self):
        if self.nosetests_arguments is None:
            self.nosetests_arguments = []
        else:
            self.nosetests_arguments = self.nosetests_arguments.split()

        self.nosetests_arguments.insert(0, os.path.basename(os.getcwd()))

    def run(self):
        import nose
        success = nose.run(argv = self.nosetests_arguments)

        print('success:', success)

        sys.exit(not success)

PARAMS['cmdclass'] = {
    'test': test,
}

PARAMS['entry_points'] = {
    'console_scripts': [
        'etest = etest:etest',
    ],
}

PARAMS['data_files'] = [
    ('share/doc/{P[name]}-{P[version]}'.format(P = PARAMS), [
        'README.rst',
    ]),
]

setup(**PARAMS)

# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

from setuptools import setup, find_packages
from codecs import open

with open(os.path.join('etest', 'information.py'), 'r', encoding = 'utf-8') as fh:
    exec(fh.read(), globals(), locals())

PARAMS = {}

PARAMS['name'] = NAME  # flake8: noqa — provided by exec
PARAMS['version'] = VERSION  # flake8: noqa — provided by exec
PARAMS['description'] = DESCRIPTION  # flake8: noqa — provided by exec

with open('README.rst', 'r', encoding = 'utf-8') as fh:
    PARAMS['long_description'] = fh.read()

PARAMS['url'] = URL  # flake8: noqa — provided by exec
PARAMS['author'] = AUTHOR  # flake8: noqa — provided by exec
PARAMS['author_email'] = AUTHOR_EMAIL  # flake8: noqa — provided by exec
PARAMS['license'] = LICENSE  # flake8: noqa — provided by exec

PARAMS['classifiers'] = [
    'Development Status :: 2 - Pre-Alpha',
    # 'Development Status :: 3 - Alpha',
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

PARAMS['packages'] = find_packages()
PARAMS['package_data'] = {
    'etest.parsers': [ 'bash.p' ],
}

PARAMS['install_requires'] = [
    'click',
    'docker-py',
    'ply',
]

PARAMS['test_suite'] = 'nose.collector'
PARAMS['tests_require'] = [
    'coverage'
    'nose',
]

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

# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

from codecs import open

from test_etest.test_fixtures import FIXTURES_DIRECTORY

BASH_TEXTS = {}

_ = {
    'bash': open(os.path.join(FIXTURES_DIRECTORY, 'scripts', '00_empty.sh'), 'r', encoding = 'utf-8').read(),
    'dictionary': {},
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)

_ = {
    'bash': open(os.path.join(FIXTURES_DIRECTORY, 'scripts', '01_comment.sh'), 'r', encoding = 'utf-8').read(),
    'dictionary': {},
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)

_ = {
    'bash': open(os.path.join(FIXTURES_DIRECTORY, 'scripts', '02_assignment.sh'), 'r', encoding = 'utf-8').read(),
    'dictionary': {
        'foo': 'bar',
    },
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)

_ = {
    'bash': open(os.path.join(FIXTURES_DIRECTORY, 'scripts', '03_array.sh'), 'r', encoding = 'utf-8').read(),
    'dictionary': {
        'foo': [
            'thing',
        ],
    },
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)

_ = {
    'bash': open(os.path.join(FIXTURES_DIRECTORY, 'scripts', '50_dangling_quote.sh'), 'r', encoding = 'utf-8').read(),
    'dictionary': {},
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('incorrect', []).append(_)

# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

from codecs import open

from test_etest.test_fixtures import FIXTURES_DIRECTORY


def script(name):
    return open(os.path.join(FIXTURES_DIRECTORY, 'scripts', name), 'r', encoding = 'utf-8').read()


BASH_TEXTS = {}

_ = {
    'name': 'empty',
    'bash': script('00_empty.sh'),
    'dictionary': {},
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('incorrect', []).append(_)
BASH_TEXTS.setdefault('incorrect_parse', []).append(_)
BASH_TEXTS.setdefault('incorrect_tokenize', []).append(_)

_ = {
    'name': 'comment',
    'bash': script('01_comment.sh'),
    'dictionary': {},
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)
BASH_TEXTS.setdefault('correct_parse', []).append(_)
BASH_TEXTS.setdefault('correct_tokenize', []).append(_)

_ = {
    'name': 'assignment',
    'bash': script('02_assignment.sh'),
    'dictionary': {
        'FOO': 'bar',
    },
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)
BASH_TEXTS.setdefault('correct_parse', []).append(_)
BASH_TEXTS.setdefault('correct_tokenize', []).append(_)

_ = {
    'name': 'assignment_array',
    'bash': script('03_assignment_array.sh'),
    'dictionary': {
        'FOO': (
            'thing',
        ),
    },
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)
BASH_TEXTS.setdefault('correct_parse', []).append(_)
BASH_TEXTS.setdefault('correct_tokenize', []).append(_)

_ = {
    'name': 'dangling_double_quote',
    'bash': script('04_dangling_double_quote.sh'),
    'dictionary': {},
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('incorrect', []).append(_)
BASH_TEXTS.setdefault('incorrect_parse', []).append(_)
BASH_TEXTS.setdefault('correct_tokenize', []).append(_)

_ = {
    'name': 'assignment_double_quoted',
    'bash': script('05_assignment_double_quoted.sh'),
    'dictionary': {
        'FOO': 'bar bar',
        'EGIT_REPO_URI': 'git://github.com/alunduil/etest.git',
    },
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)
BASH_TEXTS.setdefault('correct_parse', []).append(_)
BASH_TEXTS.setdefault('correct_tokenize', []).append(_)

_ = {
    'name': 'function_def',
    'bash': script('06_function_def.sh'),
    'dictionary': {},
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)
BASH_TEXTS.setdefault('correct_parse', []).append(_)
BASH_TEXTS.setdefault('correct_tokenize', []).append(_)

_ = {
    'name': 'expansion',
    'bash': script('07_expansion.sh'),
    'dictionary': {
        'foo': (
            'python2_7',
            'python3_3',
        ),
    },
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)
BASH_TEXTS.setdefault('correct_parse', []).append(_)
BASH_TEXTS.setdefault('correct_tokenize', []).append(_)

_ = {
    'name': 'line continuation',
    'bash': script('08_line_continuation.sh'),
    'dictionary': {},
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)
BASH_TEXTS.setdefault('correct_parse', []).append(_)
BASH_TEXTS.setdefault('correct_tokenize', []).append(_)

_ = {
    'name': 'command with path',
    'bash': script('09_command_with_path.sh'),
    'dictionary': {},
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)
BASH_TEXTS.setdefault('correct_parse', []).append(_)
BASH_TEXTS.setdefault('correct_tokenize', []).append(_)

_ = {
    'name': 'assign variable',
    'bash': script('09_assign_variable.sh'),
    'dictionary': {},
}

BASH_TEXTS.setdefault('all', []).append(_)
BASH_TEXTS.setdefault('correct', []).append(_)
BASH_TEXTS.setdefault('correct_parse', []).append(_)
BASH_TEXTS.setdefault('correct_tokenize', []).append(_)

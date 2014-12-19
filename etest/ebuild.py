# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import logging
import os
import re

from etest.lexers.bash import BashLexer, BashSyntaxError
from etest.parsers.bash import BashParser

logger = logging.getLogger(__name__)


class Ebuild(object):
    def __init__(self, path, overlay):
        self.path = path
        self.overlay = overlay

    @property
    @functools.lru_cache(1)
    def name(self):
        return os.path.dirname(self.path)

    @property
    @functools.lru_cache(1)
    def cpv(self):
        return '=' + self.name + '-' + self.version

    @property
    @functools.lru_cache(1)
    def version(self):
        _ = self.path.replace('.ebuild', '')
        _ = re.sub(r'.*?' + re.escape(self.name.split('/')[-1]) + '-', '', _)

        return _

    @property
    @functools.lru_cache(1)
    def compat(self):
        return { k.replace('_COMPAT', '').lower(): v for k, v in self.parse().items() if '_COMPAT' in k }

    @property
    @functools.lru_cache(1)
    def restrictions(self):
        return self.parse().get('RESTRICT', '').split()

    @property
    @functools.lru_cache(1)
    def use_flags(self):
        return [ re.sub(r'^[+-]', '', _) for _ in self.parse()['IUSE'].split() ]

    @functools.lru_cache(1)
    def parse(self):
        '''Convert ebuild file into a dictionary, mapping variables to values.

        Parses the ebuild file and constructs a dictionary that maps the
        variables to their values.

        Returns
        -------

        Dictionary whose keys are variables in the associated ebuild.

        '''

        parser = BashParser()
        parser.build()

        lexer = BashLexer()
        lexer.build()

        ebuild_filename = os.path.join(self.overlay.directory, self.path)

        with open(ebuild_filename, 'r') as fh:
            try:
                parser.parser.parse(
                    input = fh.read(),
                    lexer = lexer.lexer,
                )
            except BashSyntaxError as error:
                error.message = ebuild_filename + '\n' + error.message
                raise

        return parser.symbols

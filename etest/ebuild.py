# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import click
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
        _ = re.sub(r'.*?' + self.name.split('/')[-1] + '-', '', _)

        return _

    @property
    @functools.lru_cache(1)
    def compat(self):
        return { k.replace('_COMPAT', '').lower(): v for k, v in self.parse().items() if '_COMPAT' in k }

    @property
    @functools.lru_cache(1)
    def use_flags(self):
        return self.parse()['IUSE'].split()

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

        try:
            with open(os.path.join(self.overlay.directory, self.path), 'r') as fh:
                parser.parser.parse(
                    input = fh.read(),
                    lexer = lexer.lexer,
                )
        except BashSyntaxError as error:
            logger.debug('error.args: %s', error.args)

            raise click.ClickException('{0}\n{1}'.format(_, error.args[0]))

        return parser.symbols

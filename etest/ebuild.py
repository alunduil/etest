# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import click
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

        self.parsed = False

    @property
    def name(self):
        if not hasattr(self, '_name'):
            logger.debug('self.path: %s', self.path)

            self._name = os.path.dirname(self.path)

        return self._name

    @property
    def cpv(self):
        if not hasattr(self, '_cpv'):
            self._cpv = '=' + self.name + '-' + self.version

        return self._cpv

    @property
    def version(self):
        if not hasattr(self, '_version'):
            self._version = self.path.replace('.ebuild', '')
            self._version = re.sub(r'.*?' + self.name.split('/')[-1] + '-', '', self._version)

        return self._version

    @property
    def compat(self):
        if not hasattr(self, '_compat'):
            self._compat = dict([ (k.replace('_COMPAT', '').lower(), v) for k, v in self.parse().items() if '_COMPAT' in k ])

        return self._compat

    @property
    def use_flags(self):
        if not hasattr(self, '_use_flags'):
            self._use_flags = self.parse()['IUSE'].split()

        return self._use_flags

    def parse(self):
        '''Convert ebuild file into a dictionary, mapping variables to values.

        Parses the ebuild file and constructs a dictionary that maps the
        variables to their values.

        .. note::
            parse() caches the results and will not re-read the ebuild file

        Returns
        -------

        Dictionary whose keys are variables in the associated ebuild.

        '''

        if not self.parsed:
            parser = BashParser()
            parser.build()

            lexer = BashLexer()
            lexer.build()

            self._parse = {}

            logger.debug('overlay_path: %s', self.overlay.directory)

            _ = os.path.join(self.overlay.directory, self.path)

            logger.info('parsing: %s', _)

            try:
                with open(_, 'r') as fh:
                    parser.parser.parse(
                        input = fh.read(),
                        lexer = lexer.lexer,
                    )
                    self._parse = parser.symbols
            except BashSyntaxError as error:
                raise click.ClickException('{0}\n{1}'.format(_, error.args[0]))

            self.parsed = True

        return self._parse

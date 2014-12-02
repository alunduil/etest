# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import importlib
import itertools
import logging
import os
import sys

logger = logging.getLogger(__name__)


def mock(name):
    def _(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            logger.info('STARTING: mock ' + name)

            if name in self.mocks_mask:
                logger.info('STOPPING: mock ' + name + '—MASKED')

                setattr(self, 'is_mocked_' + name, False)
                return False

            func(self, *args, **kwargs)

            logger.info('STOPPING: mock ' + name)

            setattr(self, 'is_mocked_' + name, True)
            return True

        return wrapper
    return _


def import_directory(module_basename, directory, update_path = False):
    '''Load all modules in a given directory recursively.

    All python modules in the given directory will be imported.

    Parameters
    ----------

    :``module_basename``: Module name prefix for loaded modules.
    :``directory``:       Directory to recursively load python modules from.
    :``update_path``:     If True, the system path for modules is updated to
                          include ``directory``; otherwise, it is left alone.

    '''

    if update_path:
        update_path = bool(sys.path.count(directory))
        sys.path.append(directory)

    logger.info('loading submodules of %s', module_basename)
    logger.info('loading modules from %s', directory)

    filenames = itertools.chain(*[ [ os.path.join(_[0], filename) for filename in _[2] ] for _ in os.walk(directory) if len(_[2]) ])

    module_names = []
    for filename in filenames:
        if filename.endswith('.py'):
            name = filename

            name = name.replace(directory + '/', '')
            name = name.replace('__init__.py', '')
            name = name.replace('.py', '')
            name = name.replace('/', '.')
            name = name.strip('.')

            if not len(name):
                continue

            name = module_basename + '.' + name

            known_symbols = set()
            name = '.'.join([ _ for _ in name.split('.') if _ not in known_symbols and not known_symbols.add(_) ])

            if len(name):
                module_names.append(name)

    logger.debug('modules found: %s', list(module_names))

    for module_name in module_names:
        logger.info('loading module %s', module_name)

        try:
            importlib.import_module(module_name)
        except ImportError as e:
            logger.warning('failed loading %s', module_name)
            logger.exception(e)
        else:
            logger.info('successfully loaded %s', module_name)

    if update_path:
        sys.path.remove(directory)

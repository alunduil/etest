# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import docker
import itertools
import logging
import os
import uuid

from etest import overlay

logger = logging.getLogger(__name__)


class Test(object):
    def __init__(self, ebuild, test = False, base_docker_image = 'alunduil/etest:latest', **kwargs):
        self.ebuild = ebuild

        self.test = test

        self.use_flags = kwargs.get('use_flags', [])

        self.failed = False

        self.containers = []
        self.docker_images = [ base_docker_image ]

    @property
    def name(self):
        if not hasattr(self, '_name'):
            self._name = self.ebuild.name + '[' + ','.join(self.use_flags)

            if self.test:
                self._name += ',test'

            self._name += ']'

        return self._name

    @property
    def commands(self):
        if not hasattr(self, '_commands'):
            self._commands = []

            if self.test:
                self._commands.append('echo {0} test >> /etc/portage/package.env'.format(self.ebuild.name))

            self._commands.append('echo {0} {1} >> /etc/portage/package.use'.format(self.ebuild.name, ' '.join(self.use_flags)))
            self._commands.append('emerge -q {0} -f --autounmask-write'.format(self.ebuild.name))
            self._commands.append('etc-update --automode -5')
            self._commands.append('emerge -q {0}'.format(self.ebuild.name))

        return self._commands

    @property
    def environment(self):
        if not hasattr(self, '_environment'):
            self._environment = {}

            if 'python' is self.ebuild.compat:
                self.environment['PYTHON_TARGETS'] = ' '.join(self.ebuild.compat['python'])

        return self._environment

    def clean(self):
        c = docker.Client()

        for container in self.containers:
            c.remove_container(container)

        for docker_image in self.docker_images[1:]:
            c.remove_image(docker_image)

    def run(self):
        repository = 'etest/' + self.name

        c = docker.Client()

        repository, tag = self.docker_images[-1].split(':')

        c.pull(repository = repository, tag = tag)

        for command in self.commands:
            self.containers.append(uuid.uuid4())
            c.create_container(
                image = self.docker_images[-1],
                name = self.containers[-1],
                environment = self.environment,
                volumes = [
                    '/usr/portage',
                    '/overlay',
                ],
                entrypoint = '/bin/bash',
                command = command,
            )

            c.start(
                container = self.containers[-1],
                binds = {
                    self.ebuild.overlay.directory: {
                        'bind': '/overlay',
                        'ro': True,
                    },
                    # TODO: Retrive this from environment.
                    '/usr/portage': {
                        'bind': '/usr/portage',
                        'ro': True,
                    },
                },
            )

            tag = self.commands.index(command)

            self.docker_images.append(repository + ':' + tag)
            c.commit(
                self.containers[-1],
                repository = repository,
                tag = tag,
            )


class Tests(object):
    def __init__(self, ebuild_filter = ()):
        self.overlay = overlay.Overlay()

        # NOTE: raises InvalidOverlayError when necessary
        logger.debug('self.overlay.directory: %s', self.overlay.directory)

        self.ebuild_filter = [ _.replace('.ebuild', '') for _ in ebuild_filter ]

        if not len(self.ebuild_filter):
            logger.debug('os.getcwd(): %s', os.getcwd())
            logger.debug('os.path.relpath(self.overlay.directory): %s', os.path.relpath(self.overlay.directory))

            _ = os.path.relpath(self.overlay.directory)

            if _.startswith('..'):
                self.ebuild_filter.append(os.getcwd().replace(self.overlay.directory, '').strip('/'))

    @property
    def tests(self):
        if not hasattr(self, '_tests'):
            logger.info('STARTING: populate tests')

            self._tests = []

            for ebuild in self.overlay.ebuilds:
                if not len(self.ebuild_filter) or any([ _ in ebuild.name for _ in self.ebuild_filter ]):
                    self._tests.extend(self._generate_tests(ebuild))

            logger.info('STOPPING: populate tests')

        return self._tests

    def _generate_tests(self, ebuild):
        '''Generate all tests for a given ebuild.

        Prepare all tests for a given ebuild so they are ready to be run.  This
        includes finding the powerset of the USE flags and creating a runtime
        for each combination among other things.  It also includes setting
        appropriate environment variables (i.e. PYTHON_TARGETS=PYTHON_COMPAT).

        .. note::
            Later, we will add support for a test specification file to modify
            the set of tests generated by this function.

        Arguments
        ---------

        :``ebuild``: Ebuild to inspect and create various test cases for

        Returns
        -------

        Tuple of Test objects.

        '''

        logger.info('STARTING: generate tests for %s', ebuild.name)

        tests = []

        use_flags = list(ebuild.use_flags)
        use_flags.remove('test')

        logger.debug('ebuild.use_flags: %s', ebuild.use_flags)

        # TODO: Add hints file for more testing information.

        for use_flags_combination in itertools.chain.from_iterable(itertools.combinations(use_flags, _) for _ in range(len(use_flags) + 1)):
            logger.info('adding %s[%s]', ebuild.name, ','.join(use_flags_combination))

            tests.append(Test(ebuild, use_flags = use_flags_combination))

            logger.info('adding %s[test,%s]', ebuild.name, ','.join(use_flags_combination))

            tests.append(Test(ebuild, test = True, use_flags = use_flags_combination))

        logger.info('STOPPING: generate tests for %s', ebuild.name)

        return tests

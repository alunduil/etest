# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import docker
import functools
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
        self.failed_command = None

        self.time = datetime.timedelta(0)
        self.output = ''

        self.base_docker_image = base_docker_image

    @property
    @functools.lru_cache(1)
    def name(self):
        _ = self.ebuild.cpv + '[' + ','.join(self.use_flags)

        if self.test:
            if len(self.use_flags):
                _ += ','

            _ += 'test'

        _ += ']'

        return _

    @property
    @functools.lru_cache(1)
    def commands(self):
        _ = []

        if self.test:
            _.append(('bash', '-c', 'echo {0} test >> /etc/portage/package.env'.format(self.ebuild.name)))

        if len(self.use_flags):
            _.append(('bash', '-c', 'echo {0} {1} >> /etc/portage/package.use'.format(self.ebuild.name, ' '.join(self.use_flags))))

        _.append(('bash', '-c', 'emerge -q -f --autounmask-write {0} >/dev/null 2>&1 || true'.format(self.ebuild.cpv)))
        _.append(('bash', '-c', 'etc-update --automode -5 >/dev/null 2>&1'))

        _.append(('emerge', '-q', '--backtrack=130', self.ebuild.cpv))

        return _

    @property
    @functools.lru_cache(1)
    def environment(self):
        _ = {}

        if 'python' in self.ebuild.compat:
            _['PYTHON_TARGETS'] = ' '.join(self.ebuild.compat['python'])

            # Things still want python2…☹
            if 'python2_7' not in self.environment['PYTHON_TARGETS']:
                _['PYTHON_TARGETS'] += ' python2_7'

        return _

    def run(self):
        _ = docker.Client()

        image_name = self.base_docker_image

        image_id = _.inspect_image(image_name)['Id']

        repository, tag = image_name.split(':')
        _.pull(repository = repository, tag = tag)

        if image_id != _.inspect_image(image_name)['Id']:
            _.remove_image(image_id)

        repository = 'etest/' + self.name

        image_names = []

        for command in self.commands:
            logger.debug('command: %s', command)

            container_name = str(uuid.uuid4())

            logger.info('create container %s', container_name)

            _.create_container(
                image = image_name,
                name = container_name,
                environment = self.environment,
                volumes = [
                    '/overlay',
                    '/usr/portage',
                ],
                entrypoint = command[0],
                command = command[1:],
            )

            logger.info('starting container %s', container_name)

            start_time = datetime.datetime.now()

            _.start(
                container = container_name,
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

            logger.info('waiting for container %s', container_name)

            self.failed = bool(_.wait(container_name))

            self.time += datetime.datetime.now() - start_time

            self.output += _.logs(container_name).decode(encoding = 'utf-8')

            if self.failed:
                _.remove_container(container_name)
                self.failed_command = ' '.join(command)
                break

            tag = str(self.commands.index(command))

            logger.info('image container %s', container_name)

            _.commit(
                container_name,
                repository = repository,
                tag = tag,
            )
            image_name = repository + ':' + tag
            image_names.append(image_name)

            logger.info('created image %s', image_name)
            logger.info('remove container %s', container_name)

            _.remove_container(container_name)

        logger.debug('output: %s', self.output)

        for image_name in image_names:
            logger.info('remove image %s', image_name)

            _.remove_image(image_name)


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
        for ebuild in self.overlay.ebuilds:
            if not len(self.ebuild_filter) or any([ _ in ebuild.name for _ in self.ebuild_filter ]):
                for _ in self._generate_tests(ebuild):
                    yield _

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

        use_flags = list(ebuild.use_flags)
        if 'test' in use_flags:
            use_flags.remove('test')

        logger.debug('ebuild.use_flags: %s', ebuild.use_flags)

        # TODO: Add hints file for more testing information.

        for use_flags_combination in itertools.chain.from_iterable(itertools.combinations(use_flags, _) for _ in range(len(use_flags) + 1)):
            logger.info('adding %s[%s]', ebuild.name, ','.join(use_flags_combination))

            yield Test(ebuild, use_flags = use_flags_combination)

            logger.info('adding %s[test,%s]', ebuild.name, ','.join(use_flags_combination))

            yield Test(ebuild, test = True, use_flags = use_flags_combination)

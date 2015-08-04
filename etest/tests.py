# Copyright (C) 2014 by Alex Brandt <alunduil@alunduil.com>
#
# etest is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import functools
import itertools
import logging
import os
import uuid

from etest import overlay
from etest import docker

logger = logging.getLogger(__name__)


class Test(object):
    def __init__(self, ebuild, with_test_phase = False, base_docker_image = 'alunduil/etest:latest', **kwargs):
        self.ebuild = ebuild

        self.with_test_phase = with_test_phase

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

        if self.with_test_phase:
            if len(self.use_flags):
                _ += ','

            _ += 'test'

        _ += ']'

        return _

    @property
    @functools.lru_cache(1)
    def commands(self):
        _ = []

        if self.with_test_phase:
            _.append(('bash', '-c', 'echo {0} test >> /etc/portage/package.env'.format(self.ebuild.name)))

        _.append(('bash', '-c', 'echo {0} \'-*\' {1} >> /etc/portage/package.use/etest'.format(self.ebuild.name, ' '.join(self.use_flags))))

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
            if 'python2_7' not in _['PYTHON_TARGETS']:
                _['PYTHON_TARGETS'] += ' python2_7'

            # No time to test pypy right now
            if 'pypy3' in _['PYTHON_TARGETS']:
                _['PYTHON_TARGETS'] = _['PYTHON_TARGETS'].replace('pypy3', '')

            if 'pypy' in _['PYTHON_TARGETS']:
                _['PYTHON_TARGETS'] = _['PYTHON_TARGETS'].replace('pypy', '')

        return _

    def run(self):
        docker.image.pull(self.base_docker_image)

        image_name = self.base_docker_image
        image_names = []

        for command in self.commands:
            container_name = str(uuid.uuid4())

            docker.container.create(
                image = image_name,
                name = container_name,
                environment = self.environment,
                volumes = [
                    '/overlay',
                    '/usr/portage',
                ],
                entrypoint = ( command[0], ),
                command = command[1:],
            )

            start_time = datetime.datetime.now()

            is_interrupted = not docker.container.start(
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

            self.failed = is_interrupted or bool(docker.container.wait(container_name))

            self.time += datetime.datetime.now() - start_time

            # TODO: retrieve build log, etc
            self.output += docker.container.logs(container_name).decode(encoding = 'utf-8')

            if self.failed:
                docker.container.remove(container_name, v = True)
                self.failed_command = ' '.join(command)
                break

            tag_name = str(self.commands.index(command))

            docker.container.commit(
                container_name,
                repository = self.name,
                tag = tag_name,
            )

            image_name = self.name + ':' + tag_name
            image_names.append(image_name)

            docker.container.remove(container_name, v = True)

        for image_name in image_names:
            docker.image.remove(image_name)


class Tests(object):
    def __init__(self, ebuild_selector = ()):
        self.overlay = overlay.Overlay()

        # NOTE: raises InvalidOverlayError when necessary
        logger.debug('self.overlay.directory: %s', self.overlay.directory)

        self.ebuild_selector = [ _.replace('.ebuild', '') for _ in ebuild_selector ]

        if not len(self.ebuild_selector):
            _ = os.path.relpath(self.overlay.directory)

            if _.startswith('..'):
                self.ebuild_selector.append(os.getcwd().replace(self.overlay.directory, '').strip('/'))

    def __iter__(self):
        for ebuild in self.overlay.ebuilds:
            if not len(self.ebuild_selector) or any([ _ in ebuild.cpv for _ in self.ebuild_selector ]):

                use_flags = list(ebuild.use_flags)
                if 'test' in use_flags:
                    use_flags.remove('test')

                # TODO: Add hints file for more testing information.

                for use_flags_combination in itertools.chain.from_iterable(itertools.combinations(use_flags, _) for _ in range(len(use_flags) + 1)):
                    yield Test(ebuild, use_flags = use_flags_combination, with_test_phase = False)
                    if 'test' not in ebuild.restrictions:
                        yield Test(ebuild, use_flags = use_flags_combination, with_test_phase = True)

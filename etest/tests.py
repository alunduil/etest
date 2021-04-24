"""Test definitions."""
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

from etest import docker, overlay

logger = logging.getLogger(__name__)


class Test(object):
    """A single test."""

    def __init__(self, ebuild, arch, with_test_phase=False, **kwargs):
        """Construct a test."""
        self.ebuild = ebuild

        self.with_test_phase = with_test_phase

        self.use_flags = kwargs.get("use_flags", [])

        self.failed = False
        self.failed_command = None

        self.time = datetime.timedelta(0)
        self.output = ""

        self.arch = arch
        self.base_docker_image = f"alunduil/etest:{arch}"

    @functools.cached_property
    def name(self):
        """Name used to identify the test."""
        _ = self.ebuild.cpv.replace("/", "_") + "[" + ",".join(self.use_flags)

        if self.with_test_phase:
            if len(self.use_flags):
                _ += ","

            _ += "test"

        _ += "]"

        return _

    @functools.cached_property
    def commands(self):
        """Shell commands for the test."""
        _ = []

        if self.with_test_phase:
            _.append(("bash", "-c", "echo {} test >> /etc/portage/package.env".format(self.ebuild.name)))

        _.append(
            (
                "bash",
                "-c",
                "echo {} '-*' {} >> /etc/portage/package.use/etest".format(self.ebuild.name, " ".join(self.use_flags)),
            ),
        )

        _.append(
            (
                "bash",
                "-c",
                "echo {} ~{} >> /etc/portage/package.accept_keywords/etest".format(
                    self.ebuild.name,
                    self.arch,
                ),
            ),
        )

        _.append(("bash", "-c", "emerge -q -f --autounmask-write {} >/dev/null 2>&1 || true".format(self.ebuild.cpv)))
        _.append(("bash", "-c", "etc-update --automode -5 >/dev/null 2>&1"))

        _.append(("emerge", "-q", "--backtrack=130", self.ebuild.cpv))

        return _

    @functools.cached_property
    def environment(self):
        """Create a shell environment for the test."""
        _ = {}

        if "python" in self.ebuild.compat:
            _["PYTHON_TARGETS"] = " ".join(self.ebuild.compat["python"])

            # Things still want python2…☹
            if "python2_7" not in _["PYTHON_TARGETS"]:
                _["PYTHON_TARGETS"] += " python2_7"

            # No time to test pypy right now
            if "pypy3" in _["PYTHON_TARGETS"]:
                _["PYTHON_TARGETS"] = _["PYTHON_TARGETS"].replace("pypy3", "")

            if "pypy" in _["PYTHON_TARGETS"]:
                _["PYTHON_TARGETS"] = _["PYTHON_TARGETS"].replace("pypy", "")

        return _

    def run(self):
        """Run the test."""
        # docker.pull(self.base_docker_image)

        image_name = self.base_docker_image
        image_names = []

        for command in self.commands:
            container_name = str(uuid.uuid4())

            container = docker.container.create(
                overlay=self.ebuild.overlay.directory,
                image=image_name,
                name=container_name,
                environment=self.environment,
                volumes=[
                    "/overlay",
                    "/usr/portage",
                ],
                entrypoint=(command[0],),
                command=command[1:],
            )

            start_time = datetime.datetime.now()

            is_interrupted = not docker.container.start(
                container=container,
            )

            self.failed = is_interrupted or bool(docker.container.wait(container_name)["StatusCode"])

            self.time += datetime.datetime.now() - start_time

            self.output += docker.container.logs(container_name).decode(encoding="utf-8")

            if self.failed:
                docker.container.remove(container, container_name, v=True)
                self.failed_command = " ".join(command)
                break

            tag_name = str(self.commands.index(command))

            image_name = docker.container.commit(
                container=container,
                repository=self.name,
                tag=tag_name,
            )

            image_names.append(image_name)

            docker.container.remove(container, v=True)

        for image_name in image_names:
            docker.image.remove(image_name)


class Tests(object):
    """Collection of tests."""

    def __init__(self, arch, ebuild_selector=()):
        """Construct a collection of tests."""
        self.overlay = overlay.Overlay()

        self.arch = arch

        # NOTE: raises InvalidOverlayError when necessary
        logger.debug("self.overlay.directory: %s", self.overlay.directory)

        self.ebuild_selector = [_.replace(".ebuild", "") for _ in ebuild_selector]

        if not len(self.ebuild_selector):
            _ = os.path.relpath(self.overlay.directory)

            if _.startswith(".."):
                self.ebuild_selector.append(os.getcwd().replace(self.overlay.directory, "").strip("/"))

    def __iter__(self):
        """Iterate over the contained tests."""
        for ebuild in self.overlay.ebuilds:
            if not len(self.ebuild_selector) or any([_ in ebuild.cpv for _ in self.ebuild_selector]):

                use_flags = list(ebuild.use_flags)
                if "test" in use_flags:
                    use_flags.remove("test")

                # TODO: Add hints file for more testing information.

                for use_flags_combination in itertools.chain.from_iterable(
                    itertools.combinations(use_flags, _) for _ in range(len(use_flags) + 1)
                ):
                    yield Test(ebuild, use_flags=use_flags_combination, with_test_phase=False, arch=self.arch)
                    if "test" not in ebuild.restrictions:
                        yield Test(ebuild, use_flags=use_flags_combination, with_test_phase=True, arch=self.arch)

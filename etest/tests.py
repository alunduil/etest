"""Test definitions."""
import datetime
import functools
import itertools
import logging
import os
import uuid
from typing import Any, Dict, Generator, List, Optional, Tuple

import etest.ebuild
from etest import docker, overlay

logger = logging.getLogger(__name__)


class Test(object):
    """A single test."""

    def __init__(
        self,
        ebuild: etest.ebuild.Ebuild,
        with_test_phase: bool = False,
        base_docker_image: str = "alunduil/etest:latest",
        **kwargs: Any
    ) -> None:
        """Construct a test."""
        self.ebuild = ebuild

        self.with_test_phase = with_test_phase

        self.use_flags = kwargs.get("use_flags", [])

        self.failed = False
        self.failed_command: Optional[str] = None

        self.time = datetime.timedelta(0)
        self.output = ""

        self.base_docker_image = base_docker_image

    @functools.cached_property
    def name(self) -> str:
        """Name used to identify the test."""
        n = self.ebuild.cpv.replace("/", "_") + "[" + ",".join(self.use_flags)

        if self.with_test_phase:
            if len(self.use_flags):
                n += ","

            n += "test"

        n += "]"

        return n

    @functools.cached_property
    def commands(self) -> List[Any]:
        """Shell commands for the test."""
        commands = []

        if self.with_test_phase:
            commands.append(("bash", "-c", "echo {} test >> /etc/portage/package.env".format(self.ebuild.name)))

        commands.append(
            (
                "bash",
                "-c",
                "echo {} '-*' {} >> /etc/portage/package.use/etest".format(self.ebuild.name, " ".join(self.use_flags)),
            ),
        )

        commands.append(
            (
                "bash",
                "-c",
                "echo {} ~amd64 >> /etc/portage/package.accept_keywords/etest".format(
                    self.ebuild.name,
                ),
            ),
        )

        commands.append(
            ("bash", "-c", "emerge -q -f --autounmask-write {} >/dev/null 2>&1 || true".format(self.ebuild.cpv)),
        )
        commands.append(("bash", "-c", "etc-update --automode -5 >/dev/null 2>&1"))

        commands.append(("emerge", "-q", "--backtrack=130", self.ebuild.cpv))  # type: ignore

        return commands

    @functools.cached_property
    def environment(self) -> Dict[str, str]:
        """Create a shell environment for the test."""
        e = {}

        if "python" in self.ebuild.compat:
            e["PYTHON_TARGETS"] = " ".join(self.ebuild.compat["python"])

            # Things still want python2…☹
            if "python2_7" not in e["PYTHON_TARGETS"]:
                e["PYTHON_TARGETS"] += " python2_7"

            # No time to test pypy right now
            if "pypy3" in e["PYTHON_TARGETS"]:
                e["PYTHON_TARGETS"] = e["PYTHON_TARGETS"].replace("pypy3", "")

            if "pypy" in e["PYTHON_TARGETS"]:
                e["PYTHON_TARGETS"] = e["PYTHON_TARGETS"].replace("pypy", "")

        return e

    def run(self) -> None:
        """Run the test."""
        docker.pull(self.base_docker_image)

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

    def __init__(self, ebuild_selector: Optional[Tuple[str]] = None):
        """Construct a collection of tests."""
        self.overlay = overlay.Overlay()

        # NOTE: raises InvalidOverlayError when necessary
        logger.debug("self.overlay.directory: %s", self.overlay.directory)

        if ebuild_selector:
            self.ebuild_selector = [_.replace(".ebuild", "") for _ in ebuild_selector]
        else:
            self.ebuild_selector = []

        if not len(self.ebuild_selector):
            _ = os.path.relpath(self.overlay.directory)

            if _.startswith(".."):
                self.ebuild_selector.append(os.getcwd().replace(self.overlay.directory, "").strip("/"))

    def __iter__(self) -> Generator[Test, None, None]:
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
                    yield Test(ebuild, use_flags=use_flags_combination, with_test_phase=False)
                    if "test" not in ebuild.restrictions:
                        yield Test(ebuild, use_flags=use_flags_combination, with_test_phase=True)

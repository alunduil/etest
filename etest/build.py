"""Build command for etest Docker images."""

import logging
import textwrap
from pathlib import Path
from typing import List

import click
import click_log
from docker.errors import BuildError, ContainerError

from etest import docker, qemu
from etest.profile import Profile

_LOGGER = logging.getLogger()
click_log.basic_config(_LOGGER)


_libc_commands = {
    "glibc": """
        /bin/bash -c \
        'emerge-webrsync && \
        echo en_US.UTF8 UTF-8 >> /etc/locale.gen && \
        echo en_US ISO-8859-1 >> /etc/locale.gen && \
        locale-gen && \
        eselect locale set en_US.utf8'
    """,
    "musl": """
        /bin/bash -c \
        'touch /etc/portage/repos.conf/musl.conf && \
        echo \
            "[musl]
            location = /var/db/repos/musl
            sync-type = git
            sync-uri = https://github.com/gentoo-mirror/musl.git" >> /etc/portage/repos.conf/musl.conf && \
        emerge-webrsync && \
        emerge dev-vcs/git && \
        emerge --sync musl'
    """,
    "uclibc": "/bin/bash -c emerge-webrsync",
}


@click.command(name="etest-build")
@click_log.simple_verbosity_option(_LOGGER)
@click.option("-s", "--strict", is_flag=True, default=False, help="Fail on warnings.")
@click.option("--hardened/--no-hardened", default=False, help="Use a hardened profile.")
@click.option("--multilib/--no-multilib", default=True, help="Use a multilib profile.")
@click.option("--systemd/--no-systemd", default=False, help="Use a systemd profile.")
# The following could and should be excised to an architecture module that
# handles the nuances of architecture differences in Gentoo and Docker.
@click.option(
    "--architecture",
    "--arch",
    type=click.Choice(
        ["amd64", "x86", "arm64", "armv5", "armv7", "ppc64"], case_sensitive=False
    ),
    default="amd64",
    help="Architecture for the built image.",
)
@click.option(
    "--environment",
    "--env",
    multiple=True,
    help="Pass an environment variable through to Docker.",
)
@click.option(
    "--libc",
    type=click.Choice(_libc_commands.keys(), case_sensitive=False),
    default="glibc",
    help="libc for the built image.",
)
@click.option(
    "--path",
    type=click.Path(exists=True),
    default=str(Path.cwd() / "Dockerfile"),
    help="Path to the Dockerfile.",
)
@click.option("--build/--no-build", is_flag=True, default=True, help="Build an image.")
@click.option(
    "-p", "--push", is_flag=True, default=False, help="Push an image after its built."
)
def main(  # pylint: disable=too-many-arguments
    strict: bool,
    hardened: bool,
    multilib: bool,
    systemd: bool,
    architecture: str,
    environment: List[str],  # pylint: disable=unused-argument
    libc: str,
    path: str,
    build: bool,
    push: bool,
) -> None:
    """Build the etest images."""
    profile = Profile(strict, architecture, libc, hardened, multilib, systemd)

    _LOGGER.debug("Package architecture: %s.", profile.pkg_arch)
    _LOGGER.debug("Docker image: %s.", profile.docker_profile)
    _LOGGER.debug("Current profile: %s.", profile.profile)

    if build:
        _build_image(profile, path)

    if push:
        _push_image(profile)

    _LOGGER.info("etest-build has finished running.")


def _build_image(profile: Profile, path: str) -> None:
    """Build the image."""
    stage1 = None
    stage2 = None
    try:
        with qemu.qemu(profile.arch):
            _LOGGER.info("Building stage1 image.")

            _LOGGER.debug("Stage1 logs:")
            stage1 = docker.image.build(
                path=Path(path),
                buildargs={"PROFILE": profile.docker_profile},
                tag=f"etest/stage1:{profile.profile}",
            )

            _LOGGER.info("Building stage2 container.")

            _LOGGER.debug("Stage2 logs:")
            stage2 = docker.container.run(
                image=f"etest/stage1:{profile.profile}",
                command=textwrap.dedent(_libc_commands[profile.libc]),
                privileged=True,
                name=f"stage2-{profile.profile}",
            )

            _LOGGER.info("Committing the final image.")
            docker.container.commit(
                container=stage2, repository="ebuildtest/etest", tag=profile.profile
            )
    except BuildError as err:
        _LOGGER.error("Etest encountered an error while building the stage1 image.")
        _LOGGER.error("Reason: %s", err.msg)

        _LOGGER.error("Logs:")

        for line in err.build_log:
            _LOGGER.error(line.get("stream", line.get("error")))

        raise err
    except ContainerError as err:
        _LOGGER.error("Etest encountered an error while running the stage2 container.")

        msg = f"Reason: Command '{err.command}' in image '{err.image}'"
        msg += f" returned non-zero exit status {err.exit_status}:"

        _LOGGER.error(msg)
        _LOGGER.error(err.stderr)

        stage2 = err.container

        raise err
    finally:
        if stage1:
            _LOGGER.info("Cleaning up stage1 image.")
            docker.image.remove(image=f"etest/stage1:{profile.profile}", force=True)

        if stage2:
            _LOGGER.info("Cleaning up stage2 container.")
            docker.container.remove(container=stage2, force=True)


def _push_image(profile: Profile) -> None:
    """Push the built image."""
    _LOGGER.info("Starting push.")

    push_logs = docker.image.push(tag=profile.profile)

    for line in push_logs.splitlines():
        _LOGGER.debug(line)

    _LOGGER.info("Push finished.")

"""Build command for etest Docker images."""

import logging
import textwrap
from enum import Enum
from pathlib import Path
from typing import Any

import click
import click_log
from docker.errors import BuildError, ContainerError

from etest import docker, qemu
from etest.profile import Profile

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


class _libc_commands(Enum):
    glibc = """
        /bin/bash -c \
        'emerge-webrsync && \
        echo en_US.UTF8 UTF-8 >> /etc/locale.gen && \
        echo en_US ISO-8859-1 >> /etc/locale.gen && \
        locale-gen && \
        eselect locale set en_US.utf8'
    """

    musl = """
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
    """

    uclibc = "/bin/bash -c emerge-webrsync"


@click.command(name="etest-build")
@click_log.simple_verbosity_option(logger, default="WARNING")  # type: ignore
@click.option("-s", "--strict", is_flag=True, default=False, help="Fail on warnings.")
@click.option("--hardened/--no-hardened", default=False, help="Use a hardened profile.")
@click.option("--multilib/--no-multilib", default=True, help="Use a multilib profile.")
@click.option("--systemd/--no-systemd", default=False, help="Use a systemd profile.")
@click.option(
    "--architecture",
    "--arch",
    type=click.Choice(["amd64", "x86", "arm64", "armv5", "armv6", "armv7", "ppc64"], case_sensitive=False),
    default="amd64",
    help="Architecture for the built image.",
)
@click.option(
    "--libc",
    type=click.Choice([libc.name for libc in _libc_commands], case_sensitive=False),
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
@click.option("-p", "--push", is_flag=True, default=False, help="Push an image after its built.")
def main(
    strict: bool,
    hardened: bool,
    multilib: bool,
    systemd: bool,
    architecture: str,
    libc: str,
    path: str,
    build: bool,
    push: bool,
) -> None:
    """Build the etest images."""
    profile = Profile(logger, strict, architecture, libc, hardened, multilib, systemd)

    logger.debug(f"Package architecture: {profile.pkg_arch}.")
    logger.debug(f"Docker image: {profile.docker}.")
    logger.debug(f"Current profile: {profile.profile}.")

    if build:
        _build_image(profile, path)

    if push:
        push_logs = _push_image(profile)
        for line in push_logs.splitlines():
            logger.debug(line)

        logger.info("Push finished.")

    logger.info("etest-build finished running.")


def _build_image(profile: Profile, path: str) -> None:
    """Build the image."""
    stage1 = None
    stage2 = None
    try:
        with qemu.qemu(logger, profile.arch):
            logger.info("Building stage1 image.")
            stage1, stage1_logs = docker.image.build(
                path=Path(path),
                buildargs={"PROFILE": profile.docker},
                tag=f"etest/stage1:{profile.profile}",
            )

            logger.debug("Stage1 logs:")
            for line in stage1_logs:
                logger.debug(line.get("stream"))

            logger.info("Building stage2 container.")
            stage2, stage2_logs = docker.container.run(
                image=f"etest/stage1:{profile.profile}",
                command=textwrap.dedent(_libc_commands[profile.libc].value),
                privileged=True,
                name=f"stage2-{profile.profile}",
            )

            logger.debug("Stage2 logs:")
            for line in stage2_logs.split(b"\n"):
                if line:
                    logger.debug(line.decode())

            logger.info("Committing the final image.")
            docker.container.commit(container=stage2, repository="ebuildtest/etest", tag=profile.profile)
    except BuildError as e:
        logger.error("Etest encountered an error while building the stage1 image.")
        logger.error(f"Reason: {e.msg}")

        logger.error("Logs:")

        for line in e.build_log:
            logger.error(line.get("stream", line.get("error")))
        raise e
    except ContainerError as e:
        logger.error("Etest encountered an error while running the stage2 container.")

        msg = f"Reason: Command '{e.command}' in image '{e.image}'"
        msg += " returned non-zero exit status {e.exit_status}:"

        logger.error(msg)
        logger.error(f"{e.stderr}")

        stage2 = docker.common.CLIENT.containers.get(f"stage2-{profile.profile}")

        raise e
    finally:
        if stage1:
            logger.info("Cleaning up stage1 image.")
            docker.image.remove(image=f"etest/stage1:{profile.profile}", force=True)

        if stage2:
            logger.info("Cleaning up stage2 container.")
            docker.container.remove(container=stage2, force=True)


def _push_image(profile: Profile) -> Any:
    """Push the built image."""
    logger.info("Starting push.")
    return docker.image.push(tag=profile.profile)

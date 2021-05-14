"""Build command for etest Docker images."""

import textwrap
from enum import Enum
from pathlib import Path

import click  # pylint: disable=E0401

from etest import docker, qemu
from etest.profile import Profile


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
        bin/bash -c \
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
@click.option("-q", "--quiet", is_flag=True, default=False, help="Suppress all output.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Provide more output.")
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
@click.option(  # type: ignore[misc]
    "--environment",
    "--env",
    multiple=True,
    help="Pass an environment variable through to Docker.",
)
@click.option(
    "--libc",
    type=click.Choice(["glibc", "musl", "uclibc"], case_sensitive=False),
    default="glibc",
    help="libc for the built image.",
)
@click.option(
    "--path",
    type=click.Path(exists=True),
    default=str(Path.cwd() / "Dockerfile"),
    help="Path to the Dockerfile.",
)
@click.option("-p", "--push", is_flag=True, default=False, help="Push an image after its built.")
@click.option("--nobuild", is_flag=True, default=False, help="Skip building an image.")
def main(
    quiet: bool,
    verbose: bool,
    strict: bool,
    hardened: bool,
    multilib: bool,
    systemd: bool,
    architecture: str,
    environment: List[str],
    libc: str,
    path: str,
    push: bool,
    nobuild: bool,
) -> None:
    """Build the etest images."""
    profile = Profile(quiet, strict, architecture, libc, hardened, multilib, systemd)

    if verbose:
        click.echo(f"Current profile: {profile.profile}")

    if not nobuild:
        _build_image(quiet, verbose, profile, path)
    if push:
        _push_image(profile)


def _build_image(quiet: bool, verbose: bool, profile: Profile, path: str) -> None:
    """Build the image."""
    try:
        with qemu.qemu(profile.arch):
            docker.image.build(
                path=Path(path),
                buildargs={"PROFILE": profile.docker},
                tag=f"etest/stage1:{profile.profile}",
            )

            stage2 = docker.container.run(
                image=f"etest/stage1:{profile.profile}",
                command=textwrap.dedent(_libc_commands[profile.libc].value),
                privileged=True,
                name=f"stage2-{profile.profile}",
            )[0]

            docker.container.commit(container=stage2, repository="alunduil/etest", tag=profile.profile)
    finally:
        docker.image.remove(image=f"etest/stage1:{profile.profile}", force=True)

        stage2 = docker.common.CLIENT.containers.get(f"stage2-{profile.profile}")
        docker.container.remove(container=stage2, force=True)


def _push_image(profile: Profile) -> None:
    """Push the built image."""
    return docker.image.push(tag=profile.profile)

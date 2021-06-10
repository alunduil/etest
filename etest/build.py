"""Build command for etest Docker images."""
import os
from pathlib import Path

import click  # pylint: disable=E0401

from etest import docker


@click.command(name="etest-build")
@click.option("-q", "--quiet", is_flag=True, default=False, help="Suppress all output.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Provide more output.")
@click.option("--hardened/--no-hardened", default=False, help="Use a hardened profile.")
@click.option("--multilib/--no-multilib", default=True, help="Use a multilib profile.")
@click.option("--systemd/--no-systemd", default=False, help="Use a systemd profile.")
# The following could and should be excised to an architecture module that
# handles the nuances of architecture differences in Gentoo and Docker.
@click.option(  # type: ignore[misc]
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
@click.option("--path", type=Path, default=os.getcwd(), help="Path to the directory containing the Dockerfile.")
def main(
    quiet: bool,
    verbose: bool,
    hardened: bool,
    multilib: bool,
    systemd: bool,
    architecture: str,
    environment: List[str],
    libc: str,
    path: Path,
) -> None:
    """Build the etest image."""
    img_profile = build_profile(quiet, architecture, libc, hardened, multilib, systemd)
    profile = img_profile.replace("le", "")

    if verbose:
        click.echo(f"Current profile: {profile}")

    build(quiet, verbose, profile, img_profile, libc, path)


class InvalidProfileError(Exception):
    """The profile is invalid."""

    pass


def build_profile(quiet: bool, arch: str, libc: str, hardened: bool, multilib: bool, systemd: bool):
    """Check and create a profile string."""
    # Sanitize the profile
    if "arm" in arch:
        if hardened or libc != "glibc":
            raise InvalidProfileError("The ARM architecture can't use a different libc or hardened profiles.")
        if systemd and arch != "arm64":
            raise InvalidProfileError(f"{arch} doesn't support systemd.")
    elif arch == "ppc64":
        arch = "ppc64le"

        if libc == "uclibc":
            raise InvalidProfileError("The PPC64 architecture doesn't support uclibc.")
        if libc == "musl":
            raise InvalidProfileError("There are no musl base images available for PPC64.")
        if libc == "glibc" and hardened:
            raise InvalidProfileError("The PPC64 architecture doesn't support hardened glibc.")
        if systemd:
            raise InvalidProfileError("The PPC64 architecture doesn't support systemd.")

    if arch != "amd64" and not multilib:
        multilib = False
        if not quiet:
            click.echo("WARNING: --no-multilib is being overridden by an alternative libc.")

    if libc != "glibc" and not multilib:
        raise InvalidProfileError("Alternative libcs dont support no-multilib.")

    # Build the profile string
    profile = arch

    if libc != "glibc":
        profile += f"-{libc}"

    if hardened:
        profile += "-hardened"
    elif libc != "glibc":
        profile += "-vanilla"

    if not multilib:
        profile += "-nomultilib"

    if systemd:
        if profile != arch:
            raise InvalidProfileError("Systemd profiles can't use a different libc, hardened profiles or no multilib.")
        else:
            profile += "-systemd"

    return profile


def build(quiet: bool, verbose: bool, profile: str, img_profile: str, libc: str, path: Path):
    """Build the image."""
    docker.image.build(path=str(path), buildargs={"PROFILE": img_profile}, tag=f"etest/stage1:{profile}")

    if libc == "glibc":
        stage2 = docker.container.run(
            image=f"etest/stage1:{profile}",
            command="/bin/bash -c \
                    'emerge-webrsync && \
                    echo en_US.UTF8 UTF-8 >> /etc/locale.gen && \
                    echo en_US ISO-8859-1 >> /etc/locale.gen && \
                    locale-gen && \
                    eselect locale set en_US.utf8'",
            privileged=True,
            name="stage2",
        )["Container"]
    elif libc == "musl":
        stage2 = docker.container.run(
            image=f"etest/stage1:{profile}",
            command="/bin/bash -c \
                    'touch /etc/portage/repos.conf/musl.conf && \
                    echo \
                    '[musl] \
                    location = /var/db/repos/musl \
                    sync-type = git \
                    sync-uri = https://github.com/gentoo-mirror/musl.git' \
                    >> /etc/portage/repos.conf/musl.conf && \
                    emerge-webrsync && \
                    emerge dev-vcs/git && \
                    emerge --sync musl'",
            privileged=True,
            name="stage2",
        )["Container"]
    elif libc == "uclibc":
        stage2 = docker.container.run(
            image=f"etest/stage1:{profile}",
            command="/bin/bash -c \
                    'emerge-webrsync'",
            privileged=True,
            name="stage2",
        )["Container"]

    docker.container.commit(container=stage2, repository="alunduil/etest", tag=profile)

    docker.container.remove(container=stage2)
    docker.image.remove(image=f"etest/stage1:{profile}")

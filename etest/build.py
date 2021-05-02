"""Build command for etest Docker images."""
import os
from pathlib import Path

import click

from etest import docker
from etest.profile import Profile

commands = {}

commands[
    "glibc"
] = """
/bin/bash -c \
'emerge-webrsync && \
echo en_US.UTF8 UTF-8 >> /etc/locale.gen && \
echo en_US ISO-8859-1 >> /etc/locale.gen && \
locale-gen && \
eselect locale set en_US.utf8'
"""

commands[
    "musl"
] = """
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

commands["uclibc"] = "/bin/bash -c emerge-webrsync"


@click.command(name="etest-build")
@click.option("-q", "--quiet", is_flag=True, default=False, help="Suppress all output.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Provide more output.")
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
    libc: str,
    path: Path,
) -> None:
    """Build the etest image/s."""
    if not (path / "Dockerfile").is_file():
        raise FileNotFoundError(f"No Dockerfile found on {path}")

    profile = Profile(quiet, architecture, libc, hardened, multilib, systemd)
    profile.build()

    if verbose:
        click.echo(f"Current profile: {profile.profile}")

    build(quiet, verbose, profile, path)


def build(quiet: bool, verbose: bool, profile: Profile, path: Path) -> None:
    """Build the image."""
    docker.image.build(
        path=str(path),
        buildargs={"PROFILE": profile.docker_profile},
        tag=f"etest/stage1:{profile.profile}",
    )

    stage2 = docker.container.run(
        image=f"etest/stage1:{profile.profile}",
        command=commands[profile.libc],
        privileged=True,
        name=f"stage2-{profile.profile}",
    )["Container"]

    docker.container.commit(container=stage2, repository="alunduil/etest", tag=profile.profile)

    docker.container.remove(container=stage2)
    docker.image.remove(image=f"etest/stage1:{profile.profile}")

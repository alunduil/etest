"""Build command for etest Docker images."""
import os
import sys
from pathlib import Path
from typing import List

import click  # pylint: disable=E0401


@click.command(name="etest-build")  # type: ignore[misc]
@click.option("--hardened/--no-hardened", default=False, help="Use a hardened profile.")  # type: ignore[misc]
@click.option("--multilib/--no-multilib", default=True, help="Use a multilib profile.")  # type: ignore[misc]
@click.option("--systemd/--no-systemd", default=False, help="Use a systemd profile.")  # type: ignore[misc]
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
@click.option(  # type: ignore[misc]
    "--name",
    type=Path,
    default=os.path.basename(sys.argv[0]),
    help="Name of the directory?",
)
def main(  # pylint: disable=R0913
    hardened: bool,
    multilib: bool,
    systemd: bool,
    architecture: str,
    environment: List[str],
    name: Path,
) -> None:
    """Build the etest image."""
    click.echo(f"hardened: {hardened}")
    click.echo(f"multilib: {multilib}")
    click.echo(f"systemd: {systemd}")
    click.echo(f"architecture: {architecture}")
    click.echo(f"environment: {environment}")
    click.echo(f"name: {name}")

# Copyright 2022 Yu-Kai Lin. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import re
import subprocess as sp
from pathlib import Path

import click


@click.group()
def main():
    pass


_COMMAND_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def _validate_command(command: str) -> None:
    """Raise click.BadParameter if command contains characters unsafe for shell embedding."""
    if not _COMMAND_RE.match(command):
        raise click.BadParameter(
            "must match ^[A-Za-z0-9][A-Za-z0-9_-]*$",
            param_hint="'COMMAND'",
        )


def _pwsh_escape(path: str) -> str:
    """Escape single quotes in a path for use in a PowerShell single-quoted string."""
    return path.replace("'", "''")


def get_current_encoding() -> str:
    """
    Determines the current console code page encoding by executing a PowerShell command.
    Retrieve the active code page from the `chcp` command output and extract code from byte string.
    Returns:
        str: The current console code page encoding as a string.
    """
    encoding = sp.run(
        ["pwsh", "-c", "(chcp | Out-String).Split(' ')[-1].Trim()"],
        shell=False,
        capture_output=True,
        check=True,
    )
    return encoding.stdout.decode("utf-8").strip()


@main.command()
@click.argument("command")
def install(command):
    """Land the shell completion to PowerShell 7."""
    _validate_command(command)
    profile = (
        sp.run(["pwsh", "-c", "echo $PROFILE"], shell=False, capture_output=True, check=True)
        .stdout.decode(get_current_encoding())
        .strip()
    )
    profile = Path(profile)

    # Write the completion script to a local profile
    completion_varname = "_{}_COMPLETE".format(command.replace("-", "_").upper())

    completion_profile = profile.parent / ".{}_profile.ps1".format(command)
    sp.run(
        [
            "pwsh",
            "-c",
            "$env:{0} = 'pwsh_source'; {1} > '{2}'; $env:{0} = $null".format(
                completion_varname,
                command,
                _pwsh_escape(str(completion_profile)),
            ),
        ],
        shell=False,
        check=True,
    )
    sp.run(
        [
            "pwsh",
            "-c",
            # Write `& 'path'` to the profile. In a PS single-quoted string ''
            # represents a literal single quote, so '& ''{0}''' expands to
            # `& '{0}'` where {0} already has internal quotes doubled by
            # _pwsh_escape(), giving $-safe invocation regardless of path content.
            "echo '& ''{0}''' >> '{1}'".format(
                _pwsh_escape(str(completion_profile)),
                _pwsh_escape(str(profile)),
            ),
        ],
        shell=False,
        check=True,
    )

    print("Complete.")


@main.command()
@click.argument("command")
def update(command):
    """Update shell completion scripts to PowerShell 7."""
    _validate_command(command)
    profile = (
        sp.run(["pwsh", "-c", "echo $PROFILE"], shell=False, capture_output=True, check=True)
        .stdout.decode(get_current_encoding())
        .strip()
    )
    profile = Path(profile)

    # Write the completion script to a local profile
    completion_varname = "_{}_COMPLETE".format(command.replace("-", "_").upper())

    completion_profile = profile.parent / ".{}_profile.ps1".format(command)

    if not completion_profile.exists():
        print("ERROR: Cannot find existing completion profile. Try `install` instead.")
        exit(1)

    sp.run(
        [
            "pwsh",
            "-c",
            "$env:{0} = 'pwsh_source'; {1} > '{2}'; $env:{0} = $null".format(
                completion_varname,
                command,
                _pwsh_escape(str(completion_profile)),
            ),
        ],
        shell=False,
        check=True,
    )

    print("Complete.")


if __name__ == "__main__":
    main()

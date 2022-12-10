# Copyright 2022 Yu-Kai Lin. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import subprocess as sp
from pathlib import Path

import click


@click.group()
def main():
    pass


@main.command()
@click.argument("command")
def install(command):
    """Land the shell completion to PowerShell 7."""
    profile = (
        sp.run('pwsh -c "echo $PROFILE"', shell=True, capture_output=True)
        .stdout.decode()
        .strip()
    )
    profile = Path(profile)

    # Write the completion script to a local profile
    completion_varname = "_{}_COMPLETE".format(command.replace("-", "_").upper())

    completion_profile = profile.parent / ".{}_profile.ps1".format(command)
    sp.run(
        "pwsh -c \"$env:{0} = 'pwsh_source'; {1} > {2}; $env:{0} = $null\"".format(
            completion_varname, command, str(completion_profile)
        ),
        shell=True,
    )
    sp.run(
        'pwsh -c "echo \'"{}" | Invoke-Expression\' >> {}"'.format(
            str(completion_profile), str(profile)
        ),
        shell=True,
    )

    print("Complete.")


@main.command()
@click.argument("command")
def update(command):
    """Update shell completion scripts to PowerShell 7."""
    profile = (
        sp.run('pwsh -c "echo $PROFILE"', shell=True, capture_output=True)
        .stdout.decode()
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
        "pwsh -c \"$env:{0} = 'pwsh_source'; {1} > {2}; $env:{0} = $null\"".format(
            completion_varname, command, str(completion_profile)
        ),
        shell=True,
    )

    print("Complete.")


if __name__ == "__main__":
    main()

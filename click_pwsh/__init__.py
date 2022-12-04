# Copyright 2022 Yu-Kai Lin. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import click.shell_completion

from click_pwsh.shell_completion import PwshComplete

_registered = False


def support_pwsh_shell_completion() -> None:
    """Support shell completion for PowerShell 7."""
    global _registered

    if not _registered:
        click.shell_completion.add_completion_class(PwshComplete)
        _registered = True

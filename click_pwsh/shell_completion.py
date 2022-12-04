# Copyright 2022 Yu-Kai Lin. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import typing as t

from click.parser import split_arg_string
from click.shell_completion import CompletionItem, ShellComplete

_SOURCE_PWSH = """\
Register-ArgumentCompleter -Native -CommandName %(prog_name)s -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)
        $env:COMP_WORDS = $commandAst
        $imcompleteCommand = $commandAst.ToString()

        if ($cursorPosition -gt $imcompleteCommand.Length) { $cursorPosition = \
$imcompleteCommand.Length }
        $env:COMP_CWORD = @($imcompleteCommand.substring(0, \
$cursorPosition).Split(" ") | Where-Object { $_ -ne "" }).Length
        if ( $wordToComplete.Length -gt 0) { $env:COMP_CWORD -= 1 }

        $env:%(complete_var)s = "pwsh_complete"

        %(prog_name)s | ForEach-Object {
            $type, $value, $help = $_.Split(",", 3)
            if ( ![string]::IsNullOrEmpty($value) ) {
                [System.Management.Automation.CompletionResult]::new($value, \
$value, "ParameterValue", $value)
            }
        }

        $env:COMP_WORDS = $null | Out-Null
        $env:COMP_CWORD = $null | Out-Null
        $env:%(complete_var)s = $null | Out-Null
}
"""


class PwshComplete(ShellComplete):
    """Shell completion for PowerShell 7."""

    name = "pwsh"
    source_template = _SOURCE_PWSH

    def get_completion_args(self) -> t.Tuple[t.List[str], str]:
        cwords = split_arg_string(os.environ["COMP_WORDS"])
        cword = int(os.environ["COMP_CWORD"])
        args = cwords[1:cword]

        try:
            incomplete = cwords[cword]
        except IndexError:
            incomplete = ""

        return args, incomplete

    def format_completion(self, item: CompletionItem) -> str:
        return f"{item.type},{item.value},{item.help if item.help else '_'}"

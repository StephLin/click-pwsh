# `PS>` click-pwsh

[![Supported Python Versions](https://img.shields.io/pypi/pyversions/click-pwsh)](https://pypi.org/project/click-pwsh/) [![PyPI version](https://badge.fury.io/py/click-pwsh.svg)](https://badge.fury.io/py/click-pwsh)

A [click](https://github.com/pallets/click) extension to support shell completion for **[PowerShell 7](https://github.com/PowerShell/PowerShell)**.

This extension is written based on click **8.x** (i.e., the rewritten click's completion system). Be aware of your click version before using it.

Hope it can provide smooth experiences for Windows users. d(`･∀･)b

## Installation

You can get the package from PyPI:

```bash
PS> pip install click-pwsh
```

## Quickstart

Add the following code at the top of your script:

```python
from click_pwsh import support_pwsh_shell_completion
support_pwsh_shell_completion()
```

And run the following command to install the shell completion:

```bash
PS> python -m click_pwsh install foo-bar
Complete.
```

where `foo-bar` is your command name.

Then ... all done. Re-open PowerShell 7 and enjoy the shell completion!

## Update Shell Completion Scripts

If you upgrade click-pwsh, you can use the following command to update your shell completion scripts:

```bash
PS> python -m click_pwsh update foo-bar
Complete.
```

where `foo-bar` is your command name whose shell completion scripts have already installed before.

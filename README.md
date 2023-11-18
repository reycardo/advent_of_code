# Advent of Code challenge
---

## Quick start (Windows)
### Pyenv-win

1. Install pyenv-win in PowerShell.

   ```pwsh
   Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
   ```
1. Reopen PowerShell
1. Run `pyenv --version` to check if the installation was successful.
1. Run `type .python-version` to check what python version this repo uses
1. Run `pyenv install <version>` to install the python version this repo uses
1. Run `pyenv local <version>` to set a Python version as the local version
1. Run `pyenv local <version>` to set a Python version as the local version

### Poetry

1. Run `python -m venv venv` to create a venv called venv
1. Run `venv\Scripts\activate.bat` to activate the new venv
1. Run `python -m pip install -U pip setuptools poetry` to install poetry
1. Run `poetry install` to install all dependencies via poetry

And now you are ready to use this repo
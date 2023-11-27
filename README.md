# Advent of Code challenge ⭐️
![](https://img.shields.io/badge/2020_stars%20⭐-19-yellow)
![](https://img.shields.io/badge/2020_days%20completed-9-red)

![](https://img.shields.io/badge/2021_stars%20⭐-30-yellow)
![](https://img.shields.io/badge/2021_days%20completed-15-red)

![](https://img.shields.io/badge/2022_stars%20⭐-26-yellow)
![](https://img.shields.io/badge/2022_days%20completed-13-red)

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

### Poetry

1. Run `python -m venv venv` to create a venv called venv
1. Run `venv\Scripts\activate.bat` to activate the new venv
1. Run `python -m pip install -U pip setuptools poetry` to install poetry
1. Run `poetry install` to install all dependencies via poetry

And now you are ready to use this repo

## Usage
1. Make sure your venv is activated:
`venv\Scripts\activate.bat`
1. Run from root(advent_of_code):
   Example running Day1 of 2023
`python advent-of-code\src\2023\Day1\day1.py`

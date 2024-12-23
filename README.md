# Advent of Code challenge ⭐️
![](https://img.shields.io/badge/2019_stars%20⭐-8-yellow)
![](https://img.shields.io/badge/2019_days%20completed-4-red)

![](https://img.shields.io/badge/2020_stars%20⭐-19-yellow)
![](https://img.shields.io/badge/2020_days%20completed-9-red)

![](https://img.shields.io/badge/2021_stars%20⭐-30-yellow)
![](https://img.shields.io/badge/2021_days%20completed-15-red)

![](https://img.shields.io/badge/2022_stars%20⭐-26-yellow)
![](https://img.shields.io/badge/2022_days%20completed-13-red)

![](https://img.shields.io/badge/2023_stars%20⭐-33-yellow)
![](https://img.shields.io/badge/2023_days%20completed-15-red)

![](https://img.shields.io/badge/2024_stars%20⭐-43-yellow)
![](https://img.shields.io/badge/2024_days%20completed-21-red)

## Quick start (Windows)

### Pyenv-win

1. Install pyenv-win in PowerShell.

   ```pwsh
   Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
   ```
1. if error run `Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser`
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

If you fail `poetry install` because of `lz4`, download:

`https://visualstudio.microsoft.com/visual-cpp-build-tools/`

And then, run this on the directory you downloaded `vs_buildtools.exe`:
`vs_buildtools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools`

And now you are ready to use this repo

## Usage
### Getting input
Requirements:
Puzzle inputs differ by user. For this reason, you can't get your data with an unauthenticated request. Here's how to get your session cookie for aocd to use:

Login on AoC with github or whatever
Open browser's developer console (e.g. right click --> Inspect) and navigate to the Network tab
GET any input page, say adventofcode.com/2016/day/1/input, and look in the request headers.
It's a long hex string. Copy it to a plain text file at ~/.config/aocd/token.
![get_token](https://github.com/reycardo/advent_of_code//blob/master/advent-of-code/docs/images/get_aocd_token.png?raw=true)

1. Make sure your venv is activated:
`venv\Scripts\activate.bat`
1. Run get_input.py:
   Example for getting Day1 of 2023
`poetry run get_input 1 2023`

### Running Code
1. Make sure your venv is activated:
`venv\Scripts\activate.bat`
1. Run from root(advent_of_code):
   Example running Day1 of 2023
`python advent-of-code\src\2023\Day1\main.py`

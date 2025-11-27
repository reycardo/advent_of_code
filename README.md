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

![](https://img.shields.io/badge/2024_stars%20⭐-45-yellow)
![](https://img.shields.io/badge/2024_days%20completed-22-red)

## Quick Start

### Windows

*Setup instructions coming soon.*

### Mac

#### Prerequisites

- Homebrew must be installed: [Install Homebrew](https://brew.sh/)
- UV must be installed:  
  Run `brew install uv` to install uv

#### UV

1. Run `uv venv` to create a venv called .venv
1. Run `source .venv/bin/activate` to activate the new .venv
1. Run `uv pip install -e .` to install all dependencies via uv
1. Run `uv run pre-commit install` to install pre-commits locally



And now you are ready to use this repo

## Usage

1. Activate your virtual environment:
  ```sh
  source .venv/bin/activate
  ```

You can run your code in several ways:

- **From the project root:**
  ```sh
  uv run python advent_of_code/src/2024/Day1/main.py
  ```

- **From a specific day directory:**
  ```sh
  cd advent_of_code/src/2024/Day1
  uv run python main.py
  ```

- **Debug directly in VS Code or your IDE:**
  Open `main.py` and use the debugger.

## Custom Badges

To display your own Advent of Code badges:

1. Open `.github/workflows/badges.yml` in this repository.
2. Find and use your own user ID for badge generation.
3. For more details, see the [aoc-badges-action documentation](https://github.com/J0B10/aoc-badges-action).
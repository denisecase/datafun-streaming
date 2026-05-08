# datafun-streaming

[![Adaptive Interfaces](https://img.shields.io/badge/adaptive--interfaces-schema-blue?logo=github)](https://github.com/denisecase)
[![PyPI](https://img.shields.io/pypi/v/datafun-streaming?logo=pypi&label=pypi)](https://pypi.org/project/datafun-streaming/)
[![Docs Site](https://img.shields.io/badge/docs-site-blue?logo=github)](https://denisecase.github.io/datafun-streaming/)
[![Repo](https://img.shields.io/badge/repo-GitHub-black?logo=github)](https://github.com/denisecase/datafun-streaming)
[![Python 3.15+](https://img.shields.io/badge/python-3.15%2B-blue?logo=python)](https://github.com/denisecase/datafun-streaming/blob/main/pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[![CI](https://github.com/denisecase/datafun-streaming/actions/workflows/ci-python-zensical.yml/badge.svg?branch=main)](https://github.com/denisecase/datafun-streaming/actions/workflows/ci-python-zensical.yml)
[![Docs](https://github.com/denisecase/datafun-streaming/actions/workflows/deploy-zensical.yml/badge.svg?branch=main)](https://github.com/denisecase/datafun-streaming/actions/workflows/deploy-zensical.yml)
[![Links](https://github.com/denisecase/datafun-streaming/actions/workflows/links.yml/badge.svg?branch=main)](https://github.com/denisecase/datafun-streaming/actions/workflows/links.yml)

> Shared Python utilities for Kafka, DuckDB, validation, stats, and visualization
> across streaming data analytics projects.

## Command Reference

<details>
<summary>Show command reference</summary>

### In a machine terminal

Open a machine terminal where you want the project:

```shell
git clone https://github.com/denisecase/datafun-streaming

cd datafun-streaming
code .
```

### In a VS Code terminal

```shell
# reset uv cache only after suspected cache corruption or strange dependency errors
# uv cache clean

uv self update
uv python pin 3.14
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install

git add -A
uvx pre-commit run --all-files
# repeat if changes were made
git add -A
uvx pre-commit run --all-files

# do chores
uv run python -m ruff format .
uv run python -m ruff check . --fix
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.
- You do not need to add to or modify `tests/`. They are provided for example only.
- Many files are silent helpers. Explore as you like, but nothing is required.
- You do NOT not to understand everything; understanding builds naturally over time.

## Troubleshooting >>> or

If you see something like this in your terminal: `>>>` or `...`
You accidentally started Python interactive mode.
It happens.
Press `Ctrl+c` (both keys together) or `Ctrl+Z` then `Enter` on Windows.

## Example Output

```shell
| INFO | P01 | ========================
| INFO | P01 | START main()
| INFO | P01 | ========================
| INFO | P01 | ROOT_DIR = .
| INFO | P01 | DATA_DIR = data
| INFO | P01 | OUTPUT_CSV = data\sales.csv
| INFO | P01 | Streaming 3 sales to C:\Repos\streaming\datafun-streaming\data\sales.csv ...
| INFO | P01 | Watch each sale arrive. Press CTRL+C to stop early.

| INFO | P01 | (1, 81.87, 'Backpack', 'East')
| INFO | P01 | Generated formatted multi-line SUMMARY string.
| INFO | P01 | Returning the str to the calling function.
| INFO | P01 |
    Descriptive Statistics for Streaming Sales Amounts ($):
        Count of sales   : 1
        Minimum sale     : $81.87
        Maximum sale     : $81.87
        Average sale     : $81.87
        Standard deviation: $0.00

| INFO | P01 | (2, 101.58, 'Water Bottle', 'North')
| INFO | P01 | Generated formatted multi-line SUMMARY string.
| INFO | P01 | Returning the str to the calling function.
| INFO | P01 |
    Descriptive Statistics for Streaming Sales Amounts ($):
        Count of sales   : 2
        Minimum sale     : $81.87
        Maximum sale     : $101.58
        Average sale     : $91.72
        Standard deviation: $13.94

| INFO | P01 | (3, 27.15, 'Running Shoes', 'East')
| INFO | P01 | Generated formatted multi-line SUMMARY string.
| INFO | P01 | Returning the str to the calling function.
| INFO | P01 |
    Descriptive Statistics for Streaming Sales Amounts ($):
        Count of sales   : 3
        Minimum sale     : $27.15
        Maximum sale     : $101.58
        Average sale     : $70.20
        Standard deviation: $38.56

| INFO | P01 | ========================
| INFO | P01 | Producer executed successfully!
| INFO | P01 | ========================
```

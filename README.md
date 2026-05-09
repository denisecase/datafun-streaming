# datafun-streaming

[![PyPI](https://img.shields.io/pypi/v/datafun-streaming?logo=pypi&label=pypi)](https://pypi.org/project/datafun-streaming/)
[![Docs Site](https://img.shields.io/badge/docs-site-blue?logo=github)](https://denisecase.github.io/datafun-streaming/)
[![Repo](https://img.shields.io/badge/repo-GitHub-black?logo=github)](https://github.com/denisecase/datafun-streaming)
[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](https://github.com/denisecase/datafun-streaming/blob/main/pyproject.toml)
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

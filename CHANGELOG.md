# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.1.0] - 2026-05-08

### Added

- `datafun_streaming.core` - shared type aliases
  (`DataRecordDict`, `DataRecordDictList`) used across all subpackages
- `datafun_streaming.data_validation` - field-level validators
  (`validate_required_fields`, `validate_boolean_text`, `validate_datetime`,
  `validate_positive_integer`), `ValidationResult` dataclass, `make_lookup_set`,
  `validate_reference_records`, and `add_validation_errors`
- `datafun_streaming.io` - CSV and JSON file I/O utilities (`read_csv_rows`, `read_csv_as_lookup`,
  `append_csv_row`, `row_to_json`, `row_from_json`, `format_message_for_log`)
- `datafun_streaming.kafka` - Kafka producer, consumer, admin, and connection utilities built on
  `confluent-kafka`; `KafkaSettings` frozen dataclass with `.from_env()` loader
- `datafun_streaming.stats` - `RunningStats` dataclass for incremental count,
  total, mean, minimum, and maximum without storing message history
- `datafun_streaming.storage` - DuckDB utilities with schema inference,
  allowlist-validated `upsert_row`, parameterized `query_db`, and `safe_table_name` injection guard
- `datafun_streaming.visualization` - `StreamingChart` dataclass and Plotly helpers
  (`init_chart`, `update_chart`, `save_chart`) for live data visualization
- Full test suite covering all pure-Python subpackages
  (validation, IO, stats, storage, Kafka settings, Kafka error messages)
- GitHub Actions CI workflow (pre-commit, pyright, pytest, zensical docs build)
- GitHub Actions release workflow (PyPI Trusted Publishing via OIDC, GitHub Pages docs deploy)
- `pyproject.toml` with hatchling + hatch-vcs, ruff strict config, pyright basic config,
  and pytest coverage

---

## Notes on versioning and releases

- We use **SemVer**:
  - **MAJOR** - breaking changes
  - **MINOR** - backward-compatible additions
  - **PATCH** - fixes, documentation, tooling
- Versions are driven by git tags. Tag `vX.Y.Z` to release.

---

## Release Procedure (Required)

Follow these steps exactly when creating a new release.

### Task 1. Update release metadata (manual edits)

1.1. `CITATION.cff` - update `version` and `date-released`
1.2. CHANGELOG.md: add section, move unreleased entries, update links
1.3. pyproject.toml - update [tool.hatch.version].fallback-version (near the end)

### Task 2. Sync Version and Validate

```shell
uv sync --extra dev --extra docs --upgrade
git add -A
uvx pre-commit run --all-files
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

uv run python -m build
uv run python -m twine check dist/\*
```

### Task 3. Commit, tag, push

```shell
git add -A
git commit -m "Prep X.Y.Z"
git push -u origin main
```

Verify actions run on GitHub. After success:

```shell
git tag vX.Y.Z -m "X.Y.Z"
git push origin vX.Y.Z
```

## Only As Needed (delete a tag)

```shell
git tag -d vX.Z.Y
git push origin :refs/tags/vX.Z.Y
```

## Links

[Unreleased]: https://github.com/denisecase/datafun-streaming/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/denisecase/datafun-streaming/releases/tag/v0.1.0

<!-- markdownlint-enable MD024 -->

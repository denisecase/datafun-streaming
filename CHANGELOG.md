# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.7.0] - 2026-05-09

This release adds a producer-focused improvement:
Kafka settings can now control whether a topic
is cleared at producer startup, and producer
utilities now include a generic topic-preparation helper.

## Added

- Added `DEFAULT_CLEAR_TOPIC_ON_START`.
- Added `KafkaSettings.clear_topic_on_start`.
- Added support for reading `KAFKA_CLEAR_TOPIC_ON_START` from `.env`.
- Added `prepare_producer_topic(settings)` to `datafun_streaming.kafka.kafka_producer_utils`.

## Changed

- Producer topic preparation can now be handled by the imported package.
- `prepare_producer_topic(settings)`:
  - creates the topic if it does not exist;
  - keeps an existing topic when `settings.clear_topic_on_start` is false;
  - deletes and recreates the topic when `settings.clear_topic_on_start` is true.

---

## [0.6.0] - 2026-05-09

### Updated

`KafkaSettings`:

- added `DEFAULT_BROKER_ADDRESS_FAMILY` constant and
- `broker_address_family` field (default `"any"`),
- read from `KAFKA_BROKER_ADDRESS_FAMILY` env var.

`KafkaSettings.producer_config()` and `consumer_config()`:

- now include `broker.address.family` in the returned rdkafka config dict.

`get_topic_message_count()`:

- `temp_consumer` now uses `settings.broker_address_family`,
- fixing a silent bypass of address family setting
  when inspecting watermark offsets.

### Notes

WSL2 users on Windows should set `KAFKA_BROKER_ADDRESS_FAMILY=v6` in `.env`
if `localhost` resolves to `::1`
and rdkafka fails with `Connect to ipv4#127.0.0.1 failed`.

---

## [0.5.0] - 2026-05-09

### Updated

- broker family and v6

---

## [0.4.0] - 2026-05-09

### Updated

- api docs

---

## [0.3.0] - 2026-05-08

### Added

- `datafun_streaming.storage.duckdb_sql` - pure SQL string builder functions
  (`build_create_table_sql`, `build_clear_table_sql`, `build_insert_sql`)
  with no database connection required, fully testable in isolation
- Tests for all three SQL builder functions in `tests/test_duckdb_sql.py`

### Changed

- `upsert_row` now requires caller-supplied `allowed_tables: frozenset[str]`
  parameter - removes the module-level placeholder allowlist and gives
  callers full control over which tables are permitted
- Removed `_ALLOWED_TABLE_NAMES` placeholder constant from `duckdb_utils.py`
- pytest `minversion` updated to `9.0`

---

## [0.2.0] - 2026-05-08

### Changed

- updated README.md
- added `npx markdownlint-cli2 --fix` to pre-commit

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

### Task 2. Validate

```shell
uv sync --extra dev --extra docs --upgrade
git add -A
uvx pre-commit run --all-files
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build
uvx validate-pyproject[all] pyproject.toml
uv build
uv run python -m twine check dist/\*
```

### Task 3. Commit, tag, push

```shell
git add -A
git commit -m "Prep X.Y.Z"
git push -u origin main
```

Verify
[actions](https://github.com/denisecase/datafun-streaming/actions)
run on GitHub. After success:

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

[Unreleased]: https://github.com/denisecase/datafun-streaming/compare/v0.7.0...HEAD
[0.7.0]: https://github.com/denisecase/datafun-streaming/releases/tag/v0.7.0
[0.6.0]: https://github.com/denisecase/datafun-streaming/releases/tag/v0.6.0
[0.5.0]: https://github.com/denisecase/datafun-streaming/releases/tag/v0.5.0
[0.4.0]: https://github.com/denisecase/datafun-streaming/releases/tag/v0.4.0
[0.3.0]: https://github.com/denisecase/datafun-streaming/releases/tag/v0.3.0
[0.2.0]: https://github.com/denisecase/datafun-streaming/releases/tag/v0.2.0
[0.1.0]: https://github.com/denisecase/datafun-streaming/releases/tag/v0.1.0

<!-- markdownlint-enable MD024 -->

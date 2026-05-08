"""Tests for datafun_streaming.data_validation.reference."""

from datafun_streaming.data_validation.reference import (
    make_lookup_set,
    validate_reference_records,
)

# === make_lookup_set ===


def test_make_lookup_set_basic() -> None:
    records = [{"region_id": "US-MO"}, {"region_id": "US-KS"}]
    result = make_lookup_set(records, "region_id")
    assert result == {"US-MO", "US-KS"}


def test_make_lookup_set_strips_whitespace() -> None:
    records = [{"region_id": "  US-MO  "}]
    result = make_lookup_set(records, "region_id")
    assert "US-MO" in result


def test_make_lookup_set_skips_blank_values() -> None:
    records = [{"region_id": ""}, {"region_id": "US-MO"}]
    result = make_lookup_set(records, "region_id")
    assert "" not in result
    assert len(result) == 1


def test_make_lookup_set_missing_key_field() -> None:
    records = [{"other_field": "value"}]
    result = make_lookup_set(records, "region_id")
    assert result == set()


# === validate_reference_records ===


def test_validate_reference_records_valid() -> None:
    records = [{"region_id": "US-MO", "name": "Missouri"}]
    errors = validate_reference_records(
        records=records,
        required_fields=["region_id", "name"],
        label="regions.csv",
    )
    assert errors == []


def test_validate_reference_records_missing_field() -> None:
    records = [{"region_id": "US-MO"}]
    errors = validate_reference_records(
        records=records,
        required_fields=["region_id", "name"],
        label="regions.csv",
    )
    assert len(errors) == 1
    assert "regions.csv record 1" in errors[0]


def test_validate_reference_records_labels_each_row() -> None:
    records = [{"region_id": ""}, {"region_id": ""}]
    errors = validate_reference_records(
        records=records,
        required_fields=["region_id"],
        label="regions.csv",
    )
    assert any("record 1" in e for e in errors)
    assert any("record 2" in e for e in errors)

"""Tests for datafun_streaming.core.types."""

from datafun_streaming.core.types import DataRecordDict, DataRecordDictList


def test_data_record_dict_is_dict() -> None:
    record: DataRecordDict = {"sale_id": "S001", "region_id": "US-MO"}
    assert isinstance(record, dict)


def test_data_record_dict_list_is_list() -> None:
    records: DataRecordDictList = [{"sale_id": "S001"}, {"sale_id": "S002"}]
    assert isinstance(records, list)
    assert len(records) == 2

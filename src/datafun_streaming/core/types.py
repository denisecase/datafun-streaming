"""src/datafun_streaming/core/types.py.

Shared type aliases used across all datafun_streaming subpackages.
Import from here when type-hinting streaming records in any module.
"""

__all__ = [
    "DataRecordDict",
    "DataRecordDictList",
]

# One message / row / record as a dictionary of text values.
DataRecordDict = dict[str, str]

# A list of messages / rows / records.
DataRecordDictList = list[DataRecordDict]

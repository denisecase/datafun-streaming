"""Tests for datafun_streaming.stats.stats_utils."""

import math

from datafun_streaming.stats.stats_utils import RunningStats


def test_initial_state_is_empty() -> None:
    stats: RunningStats = RunningStats()
    assert stats.is_empty
    assert stats.count == 0
    assert stats.total == 0.0
    assert math.isinf(stats.minimum)
    assert math.isinf(stats.maximum)


def test_update_single_value() -> None:
    stats: RunningStats = RunningStats()
    stats.update(10.0)
    assert stats.count == 1
    assert stats.total == 10.0
    assert stats.mean == 10.0
    assert stats.minimum == 10.0
    assert stats.maximum == 10.0


def test_update_multiple_values() -> None:
    stats: RunningStats = RunningStats()
    values: list[float] = [10.0, 20.0, 30.0]
    for v in values:
        stats.update(v)
    assert stats.count == 3
    assert stats.total == 60.0
    assert stats.mean == 20.0
    assert stats.minimum == 10.0
    assert stats.maximum == 30.0


def test_update_tracks_minimum_and_maximum() -> None:
    stats: RunningStats = RunningStats()
    for v in [5.0, 1.0, 9.0, 3.0]:
        stats.update(v)
    assert stats.minimum == 1.0
    assert stats.maximum == 9.0


def test_reset_clears_all_state() -> None:
    stats: RunningStats = RunningStats()
    stats.update(42.0)
    stats.reset()
    assert stats.is_empty
    assert stats.count == 0
    assert stats.total == 0.0
    assert math.isinf(stats.minimum)
    assert math.isinf(stats.maximum)


def test_summary_when_empty() -> None:
    stats: RunningStats = RunningStats()
    assert "no values" in stats.summary()


def test_summary_when_populated() -> None:
    stats: RunningStats = RunningStats()
    stats.update(100.0)
    summary = stats.summary()
    assert "count=1" in summary
    assert "mean=" in summary
    assert "minimum=" in summary
    assert "maximum=" in summary


def test_is_empty_false_after_update() -> None:
    stats: RunningStats = RunningStats()
    stats.update(1.0)
    assert not stats.is_empty

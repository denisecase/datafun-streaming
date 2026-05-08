"""stats/stats_utils.py.

Running statistics for streaming data.

Provides a RunningStats class that tracks count, sum, mean, min, and max
for a stream of numeric values without storing the full history.

This is domain-agnostic: it works on any numeric field from any message.
Pass it a value on each message and read the current statistics at any time.

Author: Denise Case
Date: 2026-05
"""

# === IMPORTS ===

from dataclasses import dataclass

# === EXPORTS ===

__all__ = [
    "RunningStats",
]

# === DEFINE RUNNING STATS CLASS ===


@dataclass
class RunningStats:
    """Accumulates running statistics for a stream of numeric values.

    Updates incrementally (one value at a time) without storing history.
    Safe to use inside a message processing loop.

    Do not use min and max as they would conflict with
    built-in functions.
    Access minimum and maximum values
    via the minimum and maximum attributes.

    Attributes:
        count: Number of values received so far.
        total: Running sum of all values.
        mean:  Running mean of all values.
        minimum:   Minimum value seen so far.
        maximum:   Maximum value seen so far.

    Example:
        stats = RunningStats()
        for message in messages:
            stats.update(message["total"])
            print(f"count={stats.count}  mean={stats.mean:.2f}")
    """

    count: int = 0
    total: float = 0.0
    mean: float = 0.0
    minimum: float = float("inf")
    maximum: float = float("-inf")

    def update(self, value: float) -> None:
        """Update statistics with one new value.

        Arguments:
            value: The new numeric value to include.

        Returns:
            None.
        """
        self.count += 1
        self.total += value
        self.mean = self.total / self.count
        if value < self.minimum:
            self.minimum = value
        if value > self.maximum:
            self.maximum = value

    def reset(self) -> None:
        """Reset all statistics to their initial state.

        Use this to start a new window or clear accumulated state.

        Returns:
            None.
        """
        self.count = 0
        self.total = 0.0
        self.mean = 0.0
        self.minimum = float("inf")
        self.maximum = float("-inf")

    @property
    def is_empty(self) -> bool:
        """Return True if no values have been received yet."""
        return self.count == 0

    def summary(self) -> str:
        """Return a formatted summary string for logging.

        Returns:
            A single-line string with all current statistics.
        """
        if self.is_empty:
            return "RunningStats: no values received yet."
        return (
            f"count={self.count}  "
            f"total={self.total:,.2f}  "
            f"mean={self.mean:,.2f}  "
            f"minimum={self.minimum:,.2f}  "
            f"maximum={self.maximum:,.2f}"
        )

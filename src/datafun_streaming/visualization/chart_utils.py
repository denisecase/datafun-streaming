"""src/datafun_streaming/visualization/chart_utils.py.

Chart utilities for streaming data.

Provides functions to create, update, and save a line chart
that accumulates data points as messages are consumed.

Uses Plotly to generate an interactive HTML chart.
The chart is updated in memory as each message arrives
and saved to disk at the end of the consume loop (Section C4).

This is domain-agnostic: pass any numeric field and any label.
The chart does not know what it is charting.

Author: Denise Case
Date: 2026-05
"""

# === IMPORTS ===

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import plotly.graph_objects as go

# === EXPORTS ===

__all__ = [
    "StreamingChart",
    "init_chart",
    "update_chart",
    "save_chart",
]

# === DEFINE CHART DATA CLASS ===


@dataclass
class StreamingChart:
    """Holds chart state for a single line series.

    Updated incrementally as messages arrive.
    Rendered to HTML when save_chart() is called.

    Attributes:
        title:    Chart title shown at the top.
        x_label:  Label for the x-axis.
        y_label:  Label for the y-axis.
        x_values: Accumulated x-axis values (e.g. message count).
        y_values: Accumulated y-axis values (e.g. running total).
    """

    title: str
    x_label: str
    y_label: str
    x_values: list[int | float | str] = field(default_factory=list)
    y_values: list[float] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        """Return True if no data points have been added yet."""
        return len(self.x_values) == 0


# === DEFINE CHART FUNCTIONS ===


def init_chart(
    *,
    title: str,
    x_label: str,
    y_label: str,
) -> StreamingChart:
    """Create a new empty StreamingChart.

    Arguments:
        title:   Chart title.
        x_label: Label for the x-axis.
        y_label: Label for the y-axis.

    Returns:
        An empty StreamingChart ready to receive data points.
    """
    return StreamingChart(title=title, x_label=x_label, y_label=y_label)


def update_chart(
    chart: StreamingChart,
    row: dict[str, Any],
    *,
    x_field: str = "_kafka_offset",
    y_field: str = "total",
) -> None:
    """Add one data point to the chart from a message row.

    Arguments:
        chart:   The StreamingChart to update.
        row:     The enriched message row.
        x_field: The row field to use as the x-axis value.
                 Defaults to _kafka_offset (message sequence number).
        y_field: The row field to use as the y-axis value.
                 Defaults to total (post-tax total price).

    Returns:
        None.
    """
    x_value = row.get(x_field, len(chart.x_values))
    y_value = row.get(y_field, 0.0)

    chart.x_values.append(x_value)
    chart.y_values.append(float(y_value))


def save_chart(chart: StreamingChart, path: Path) -> None:
    """Render the chart to an interactive HTML file.

    Arguments:
        chart: The StreamingChart to render.
        path:  Output file path. Must end in .html.

    Returns:
        None.
    """
    if chart.is_empty:
        return

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart.x_values,
            y=chart.y_values,
            mode="lines+markers",
            name=chart.y_label,
            line={"width": 2},
            marker={"size": 4},
        )
    )

    fig.update_layout(
        title=chart.title,
        xaxis_title=chart.x_label,
        yaxis_title=chart.y_label,
        hovermode="x unified",
        template="plotly_white",
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(path))

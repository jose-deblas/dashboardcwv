"""
View models for chart data.

Framework-agnostic chart configuration and data structures.
These models contain all information needed to render charts in any
charting library (Plotly, Chart.js, D3, etc.).
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass(frozen=True)
class TimeSeriesDataPoint:
    """
    Single point in a time series.

    Contains date, value, and optional label for multi-series charts.
    """

    date: date
    value: float
    label: Optional[str] = None  # For multi-series (e.g., brand name)


@dataclass(frozen=True)
class TimeSeriesViewModel:
    """
    Complete time series for a chart.

    Contains data points and styling information for a single series.
    Framework-agnostic - can be adapted to any charting library.
    """

    series_name: str
    data_points: List[TimeSeriesDataPoint]
    color: Optional[str] = None  # Color name or hex code
    line_width: int = 2
    marker_size: int = 4


@dataclass(frozen=True)
class ChartViewModel:
    """
    Complete chart configuration.

    Contains all series, styling, and threshold information needed
    to render a chart in any framework.
    """

    title: str
    series: List[TimeSeriesViewModel]
    y_axis_label: str
    show_thresholds: bool
    red_threshold: Optional[float] = None
    green_threshold: Optional[float] = None
    height: int = 500

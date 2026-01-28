"""
View models for performance section.

Framework-agnostic presentation data structures with all values pre-formatted
and ready for display. These models contain no business logic, only
presentation-ready data.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class MetricCardViewModel:
    """
    View model for a single metric card display.

    All values are pre-formatted strings ready for display.
    """

    label: str
    value: str  # Pre-formatted string (e.g., "65.00", "N/A")
    delta: Optional[str] = None  # Pre-formatted with sign (e.g., "+5.20", "-2.10")
    delta_color: Optional[str] = None  # Color hint: "green", "red", "neutral"
    help_text: Optional[str] = None


@dataclass(frozen=True)
class DeviceMetricsViewModel:
    """
    View model for device-specific metrics display.

    Contains three metric cards (target, start date, end date) plus
    growth rate display. All values pre-formatted.
    """

    device_label: str  # "Mobile" or "Desktop"
    target_card: MetricCardViewModel
    start_date_card: MetricCardViewModel
    end_date_card: MetricCardViewModel
    growth_rate_display: str  # Pre-formatted: "+12.34%", "N/A"
    growth_rate_color: str  # "green", "red", "neutral"
    has_data: bool  # True if any score data exists


@dataclass(frozen=True)
class PerformanceViewModel:
    """
    Complete view model for performance section.

    Contains all data needed to render the performance section including
    mobile and desktop metrics, filter displays, and time series availability.
    """

    mobile: DeviceMetricsViewModel
    desktop: DeviceMetricsViewModel
    active_filters_display: List[str]  # Pre-formatted filter strings
    has_time_series_data: bool  # True if time series charts should be shown

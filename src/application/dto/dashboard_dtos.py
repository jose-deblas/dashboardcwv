"""
Dashboard Data Transfer Objects.

This module contains DTOs for transferring dashboard data between layers.
Following Clean Architecture principles with immutable dataclasses.
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass(frozen=True)
class FilterCriteria:
    """
    Criteria for filtering dashboard data.

    All filter fields are optional. None means no filter applied for that field.

    Note: Validation moved to FilterValidator in application.validation module.
    Use FilterValidator.validate_date_range() before creating this DTO.
    """

    start_date: date
    end_date: date
    brands: Optional[List[str]] = None
    countries: Optional[List[str]] = None
    page_types: Optional[List[str]] = None


@dataclass(frozen=True)
class DeviceMetrics:
    """
    Performance metrics for a specific device.

    Pure data container - no presentation logic.

    Note: Presentation logic (delta, growth_rate, colors, targets) moved to
    PerformancePresenter in presentation.presenters module. This DTO now contains
    only raw business data.
    """

    device: str
    start_score: Optional[float]
    end_score: Optional[float]


@dataclass(frozen=True)
class PerformanceMetrics:
    """
    Aggregated performance metrics for the selected filters.
    """

    mobile_metrics: DeviceMetrics
    desktop_metrics: DeviceMetrics
    filter_criteria: FilterCriteria


@dataclass(frozen=True)
class TimeSeriesPoint:
    """
    A single point in a time series for performance data.
    """

    execution_date: date
    avg_performance_score: Optional[float]
    brand: Optional[str] = None  # None means aggregated across all brands


@dataclass(frozen=True)
class BrandRanking:
    """
    Ranking information for a brand.
    """

    brand: str
    avg_performance_score: float
    rank: int
    is_target_brand: bool  # True if brand is a target brand in the filter criteria

    def __post_init__(self):
        """Validate brand ranking."""
        if self.rank < 1:
            raise ValueError("rank must be >= 1")
        if self.avg_performance_score < 0 or self.avg_performance_score > 100:
            raise ValueError("avg_performance_score must be between 0 and 100")


@dataclass(frozen=True)
class CompetitorData:
    """
    Competitor analysis data including rankings and time series.
    """

    device: str
    rankings: List[BrandRanking]
    time_series: List[TimeSeriesPoint]
    filter_criteria: FilterCriteria


@dataclass(frozen=True)
class FilterOptions:
    """
    Available options for dashboard filters.
    """

    min_date: Optional[date]
    max_date: Optional[date]
    brands: List[str]
    countries: List[str]
    page_types: List[str]

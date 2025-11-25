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
    """

    start_date: date
    end_date: date
    brands: Optional[List[str]] = None
    countries: Optional[List[str]] = None
    page_types: Optional[List[str]] = None

    def __post_init__(self):
        """Validate filter criteria."""
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before or equal to end_date")


@dataclass(frozen=True)
class DeviceMetrics:
    """
    Performance metrics for a specific device.
    """

    device: str
    start_score: Optional[float]
    end_score: Optional[float]

    @property
    def delta(self) -> Optional[float]:
        """
        Calculate the change in score from start to end.

        Returns:
            Score delta (end - start), or None if either score is missing.
        """
        if self.start_score is None or self.end_score is None:
            return None
        return self.end_score - self.start_score

    @property
    def traffic_light(self) -> str:
        """
        Determine traffic light color based on score delta.

        Returns:
            'green' for positive change, 'red' for negative, 'amber' for no change or missing data.
        """
        delta = self.delta
        if delta is None:
            return "amber"
        if delta > 0:
            return "green"
        elif delta < 0:
            return "red"
        else:
            return "amber"


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

"""
Use case for retrieving performance data.

This module implements the business logic for fetching performance
metrics and time series data for the dashboard.
"""

from typing import List

from src.application.dto.dashboard_dtos import (
    DeviceMetrics,
    FilterCriteria,
    PerformanceMetrics,
    TimeSeriesPoint,
)
from src.domain.repositories.dashboard_repository import DashboardRepository


class GetPerformanceDataUseCase:
    """
    Use case for retrieving performance data.

    This use case orchestrates fetching performance metrics for both
    mobile and desktop devices, including start/end comparisons and
    time series data.
    """

    def __init__(self, dashboard_repository: DashboardRepository):
        """
        Initialize use case with repository dependency.

        Args:
            dashboard_repository: Repository for dashboard data access
        """
        self._repository = dashboard_repository

    def execute(self, filter_criteria: FilterCriteria) -> PerformanceMetrics:
        """
        Execute the use case to retrieve performance data.

        Args:
            filter_criteria: Filters to apply to the data query

        Returns:
            PerformanceMetrics DTO containing device-specific metrics

        Raises:
            RuntimeError: If repository operations fail
        """
        # Get mobile metrics
        mobile_start = self._repository.get_performance_metrics_by_date(
            target_date=filter_criteria.start_date,
            device="mobile",
            brands=filter_criteria.brands,
            countries=filter_criteria.countries,
            page_types=filter_criteria.page_types,
        )

        mobile_end = self._repository.get_performance_metrics_by_date(
            target_date=filter_criteria.end_date,
            device="mobile",
            brands=filter_criteria.brands,
            countries=filter_criteria.countries,
            page_types=filter_criteria.page_types,
        )

        # Get desktop metrics
        desktop_start = self._repository.get_performance_metrics_by_date(
            target_date=filter_criteria.start_date,
            device="desktop",
            brands=filter_criteria.brands,
            countries=filter_criteria.countries,
            page_types=filter_criteria.page_types,
        )

        desktop_end = self._repository.get_performance_metrics_by_date(
            target_date=filter_criteria.end_date,
            device="desktop",
            brands=filter_criteria.brands,
            countries=filter_criteria.countries,
            page_types=filter_criteria.page_types,
        )

        # Create device metrics
        mobile_metrics = DeviceMetrics(
            device="mobile", start_score=mobile_start, end_score=mobile_end
        )

        desktop_metrics = DeviceMetrics(
            device="desktop", start_score=desktop_start, end_score=desktop_end
        )

        return PerformanceMetrics(
            mobile_metrics=mobile_metrics,
            desktop_metrics=desktop_metrics,
            filter_criteria=filter_criteria,
        )

    def get_time_series(
        self, filter_criteria: FilterCriteria, device: str
    ) -> List[TimeSeriesPoint]:
        """
        Get time series data for a specific device.

        Args:
            filter_criteria: Filters to apply to the data query
            device: Device type ('mobile' or 'desktop')

        Returns:
            List of TimeSeriesPoint DTOs

        Raises:
            ValueError: If device is not 'mobile' or 'desktop'
            RuntimeError: If repository operations fail
        """
        if device not in ["mobile", "desktop"]:
            raise ValueError("device must be 'mobile' or 'desktop'")

        results = self._repository.get_performance_time_series(
            start_date=filter_criteria.start_date,
            end_date=filter_criteria.end_date,
            device=device,
            brands=filter_criteria.brands,
            countries=filter_criteria.countries,
            page_types=filter_criteria.page_types,
        )

        return [
            TimeSeriesPoint(
                execution_date=row["execution_date"],
                avg_performance_score=row["avg_performance_score"],
            )
            for row in results
        ]

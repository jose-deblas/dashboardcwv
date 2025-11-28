"""
Use case for retrieving competitor data.

This module implements the business logic for fetching competitor
rankings and time series data for the dashboard.
"""

from typing import List

from src.application.dto.dashboard_dtos import (
    BrandRanking,
    CompetitorData,
    FilterCriteria,
    TimeSeriesPoint,
)
from src.domain.repositories.brand_repository import BrandRepository
from src.domain.repositories.dashboard_repository import DashboardRepository


class GetCompetitorDataUseCase:
    """
    Use case for retrieving competitor data.

    This use case orchestrates fetching brand rankings and time series
    data for competitor analysis.
    """

    def __init__(
        self,
        dashboard_repository: DashboardRepository,
        brand_repository: BrandRepository,
    ):
        """
        Initialize use case with repository dependencies.

        Args:
            dashboard_repository: Repository for dashboard data access
            brand_repository: Repository for brand data access
        """
        self._repository = dashboard_repository
        self._brand_repository = brand_repository

    def execute(self, filter_criteria: FilterCriteria, device: str) -> CompetitorData:
        """
        Execute the use case to retrieve competitor data for a specific device.

        Args:
            filter_criteria: Filters to apply to the data query
            device: Device type ('mobile' or 'desktop')

        Returns:
            CompetitorData DTO containing rankings and time series

        Raises:
            ValueError: If device is not 'mobile' or 'desktop'
            RuntimeError: If repository operations fail
        """
        if device not in ["mobile", "desktop"]:
            raise ValueError("device must be 'mobile' or 'desktop'")

        # Convert to BrandRanking DTOs
        rankings = self.get_rankings(filter_criteria, device)

        # Get brands to include in time series (all brands in rankings)
        brands = [r.brand for r in rankings]

        # Get time series data for all brands in ranking
        time_series_data = self._repository.get_brand_time_series(
            start_date=filter_criteria.start_date,
            end_date=filter_criteria.end_date,
            device=device,
            brands=brands,
            countries=filter_criteria.countries,
            page_types=filter_criteria.page_types,
        )

        # Convert to TimeSeriesPoint DTOs
        time_series = [
            TimeSeriesPoint(
                execution_date=row["execution_date"],
                avg_performance_score=row["avg_performance_score"],
                brand=row["brand"],
            )
            for row in time_series_data
        ]

        return CompetitorData(
            device=device,
            rankings=rankings,
            time_series=time_series,
            filter_criteria=filter_criteria,
        )

    def get_rankings(
        self, filter_criteria: FilterCriteria, device: str
    ) -> List[BrandRanking]:
        """
        Get only the brand rankings (without time series).

        Args:
            filter_criteria: Filters to apply to the data query
            device: Device type ('mobile' or 'desktop')

        Returns:
            List of BrandRanking DTOs

        Raises:
            ValueError: If device is not 'mobile' or 'desktop'
            RuntimeError: If repository operations fail
        """
        if device not in ["mobile", "desktop"]:
            raise ValueError("device must be 'mobile' or 'desktop'")

        rankings_data = self._repository.get_brand_rankings(
            target_date=filter_criteria.end_date,
            device=device,
            countries=filter_criteria.countries,
            page_types=filter_criteria.page_types,
            limit=3,
        )

        # Get target brands for comparison
        target_brands = self._brand_repository.get_target_brands()

        return [
            BrandRanking(
                brand=row["brand"],
                avg_performance_score=row["avg_performance_score"],
                rank=row["ranking_position"],
                is_target_brand=row["brand"] in target_brands,
            )
            for row in rankings_data
        ]

"""
Use case for retrieving available filter options.

This module implements the business logic for fetching available
filter options from the database for the dashboard.
"""

from src.application.dto.dashboard_dtos import FilterOptions
from src.domain.repositories.dashboard_repository import DashboardRepository


class GetFilterOptionsUseCase:
    """
    Use case for retrieving available filter options.

    This use case orchestrates fetching all available filter values
    (brands, countries, page types, date range) from the repository.
    """

    def __init__(self, dashboard_repository: DashboardRepository):
        """
        Initialize use case with repository dependency.

        Args:
            dashboard_repository: Repository for dashboard data access
        """
        self._repository = dashboard_repository

    def execute(self) -> FilterOptions:
        """
        Execute the use case to retrieve filter options.

        Returns:
            FilterOptions DTO containing all available filter values

        Raises:
            RuntimeError: If repository operations fail
        """
        min_date, max_date = self._repository.get_date_range()
        brands = self._repository.get_target_brands()
        countries = self._repository.get_available_countries()
        page_types = self._repository.get_available_page_types()

        return FilterOptions(
            min_date=min_date,
            max_date=max_date,
            brands=brands,
            countries=countries,
            page_types=page_types,
        )

"""
Dashboard repository interface.

This module defines the abstract interface for dashboard data access operations.
Following the Repository Pattern from Clean Architecture.
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, List, Optional, Tuple


class DashboardRepository(ABC):
    """
    Abstract repository interface for dashboard data operations.

    This interface defines the contract for accessing aggregated
    Core Web Vitals data for dashboard visualizations.
    """

    @abstractmethod
    def get_date_range(self) -> Tuple[Optional[date], Optional[date]]:
        """
        Get the minimum and maximum execution dates available in the database.

        Returns:
            Tuple containing (min_date, max_date). Returns (None, None) if no data exists.
        """
        pass

    @abstractmethod
    def get_available_brands(self) -> List[str]:
        """
        Get list of distinct brands available in the database.

        Returns:
            List of brand names, sorted alphabetically.
        """
        pass

    @abstractmethod
    def get_available_countries(self) -> List[str]:
        """
        Get list of distinct countries available in the database.

        Returns:
            List of country IDs, sorted alphabetically.
        """
        pass

    @abstractmethod
    def get_available_page_types(self) -> List[str]:
        """
        Get list of distinct page types available in the database.

        Returns:
            List of page types, sorted alphabetically.
        """
        pass

    @abstractmethod
    def get_performance_metrics_by_date(
        self,
        target_date: date,
        device: str,
        brands: Optional[List[str]] = None,
        countries: Optional[List[str]] = None,
        page_types: Optional[List[str]] = None,
    ) -> Optional[float]:
        """
        Get average performance score for a specific date with optional filters.

        Args:
            target_date: The date to query
            device: Device type ('mobile' or 'desktop')
            brands: Optional list of brands to filter by
            countries: Optional list of country IDs to filter by
            page_types: Optional list of page types to filter by

        Returns:
            Average performance score, or None if no data exists.
        """
        pass

    @abstractmethod
    def get_performance_time_series(
        self,
        start_date: date,
        end_date: date,
        device: str,
        brands: Optional[List[str]] = None,
        countries: Optional[List[str]] = None,
        page_types: Optional[List[str]] = None,
    ) -> List[Dict]:
        """
        Get performance score time series data with optional filters.

        Args:
            start_date: Start of date range
            end_date: End of date range
            device: Device type ('mobile' or 'desktop')
            brands: Optional list of brands to filter by
            countries: Optional list of country IDs to filter by
            page_types: Optional list of page types to filter by

        Returns:
            List of dictionaries with keys: execution_date, avg_performance_score
            Sorted by execution_date ascending.
        """
        pass

    @abstractmethod
    def get_brand_rankings(
        self,
        target_date: date,
        device: str,
        countries: Optional[List[str]] = None,
        page_types: Optional[List[str]] = None,
        limit: int = 3,
    ) -> List[Dict]:
        """
        Get brand rankings by average performance score for a specific date.

        This returns the top N brands plus target brands if they're not in the top N.

        Args:
            target_date: The date to query
            device: Device type ('mobile' or 'desktop')
            countries: Optional list of country IDs to filter by
            page_types: Optional list of page types to filter by
            limit: Number of top brands to return (default: 3)

        Returns:
            List of dictionaries with keys: brand, avg_performance_score, rank
            Sorted by avg_performance_score descending.
        """
        pass

    @abstractmethod
    def get_brand_time_series(
        self,
        start_date: date,
        end_date: date,
        device: str,
        brands: List[str],
        countries: Optional[List[str]] = None,
        page_types: Optional[List[str]] = None,
    ) -> List[Dict]:
        """
        Get performance score time series data for specific brands.

        Args:
            start_date: Start of date range
            end_date: End of date range
            device: Device type ('mobile' or 'desktop')
            brands: List of brands to include
            countries: Optional list of country IDs to filter by
            page_types: Optional list of page types to filter by

        Returns:
            List of dictionaries with keys: execution_date, brand, avg_performance_score
            Sorted by execution_date, brand ascending.
        """
        pass

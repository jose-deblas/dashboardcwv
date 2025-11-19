"""Core Web Vitals Repository interface."""
from abc import ABC, abstractmethod
from datetime import date
from typing import List

from src.domain.entities.core_web_vitals import CoreWebVitals


class CoreWebVitalsRepository(ABC):
    """Abstract repository for Core Web Vitals operations."""

    @abstractmethod
    def add(self, metrics: CoreWebVitals) -> None:
        """
        Add Core Web Vitals metrics to the repository.

        Args:
            metrics: The CoreWebVitals entity to add

        Raises:
            DuplicateRecordException: If metrics already exist for url_id and execution_date
            RepositoryException: If insertion fails
        """
        pass

    @abstractmethod
    def exists(self, url_id: int, execution_date: date) -> bool:
        """
        Check if metrics exist for a given URL and date.

        Args:
            url_id: The URL identifier
            execution_date: The date to check

        Returns:
            True if metrics exist, False otherwise

        Raises:
            RepositoryException: If check fails
        """
        pass

    @abstractmethod
    def get_by_url_and_date(self, url_id: int, execution_date: date) -> CoreWebVitals:
        """
        Retrieve metrics for a specific URL and date.

        Args:
            url_id: The URL identifier
            execution_date: The date to retrieve

        Returns:
            CoreWebVitals entity

        Raises:
            RepositoryException: If metrics not found or retrieval fails
        """
        pass

    @abstractmethod
    def get_urls_without_data_for_date(self, execution_date: date) -> List[int]:
        """
        Get list of URL IDs that don't have metrics for the specified date.

        Args:
            execution_date: The date to check

        Returns:
            List of URL IDs without metrics for the date

        Raises:
            RepositoryException: If query fails
        """
        pass

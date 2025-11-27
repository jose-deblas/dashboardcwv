"""
Unit tests for GetFilterOptionsUseCase.
"""

from datetime import date
from unittest.mock import Mock

import pytest

from src.application.use_cases.dashboard.get_filter_options_use_case import (
    GetFilterOptionsUseCase,
)
from src.domain.repositories.dashboard_repository import DashboardRepository


class TestGetFilterOptionsUseCase:
    """Test suite for GetFilterOptionsUseCase."""

    @pytest.fixture
    def mock_repository(self) -> Mock:
        """Create a mock dashboard repository."""
        return Mock(spec=DashboardRepository)

    @pytest.fixture
    def use_case(self, mock_repository: Mock) -> GetFilterOptionsUseCase:
        """Create use case with mocked repository."""
        return GetFilterOptionsUseCase(dashboard_repository=mock_repository)

    def test_execute_returns_filter_options(
        self, use_case: GetFilterOptionsUseCase, mock_repository: Mock
    ):
        """Test that execute returns FilterOptions with all data."""
        # Arrange
        mock_repository.get_date_range.return_value = (
            date(2024, 1, 1),
            date(2024, 12, 31),
        )
        mock_repository.get_target_brands.return_value = ["Caprabo", "Lidl"]
        mock_repository.get_available_countries.return_value = ["ES", "DE", "FR"]
        mock_repository.get_available_page_types.return_value = ["home", "product"]

        # Act
        result = use_case.execute()

        # Assert
        assert result.min_date == date(2024, 1, 1)
        assert result.max_date == date(2024, 12, 31)
        assert result.brands == ["Caprabo", "Lidl"]
        assert result.countries == ["ES", "DE", "FR"]
        assert result.page_types == ["home", "product"]

        # Verify repository methods were called
        mock_repository.get_date_range.assert_called_once()
        mock_repository.get_target_brands.assert_called_once()
        mock_repository.get_available_countries.assert_called_once()
        mock_repository.get_available_page_types.assert_called_once()

    def test_execute_handles_no_data(
        self, use_case: GetFilterOptionsUseCase, mock_repository: Mock
    ):
        """Test that execute handles case when no data exists."""
        # Arrange
        mock_repository.get_date_range.return_value = (None, None)
        mock_repository.get_target_brands.return_value = []
        mock_repository.get_available_countries.return_value = []
        mock_repository.get_available_page_types.return_value = []

        # Act
        result = use_case.execute()

        # Assert
        assert result.min_date is None
        assert result.max_date is None
        assert result.brands == []
        assert result.countries == []
        assert result.page_types == []

    def test_execute_propagates_repository_errors(
        self, use_case: GetFilterOptionsUseCase, mock_repository: Mock
    ):
        """Test that repository errors are propagated to caller."""
        # Arrange
        mock_repository.get_date_range.side_effect = RuntimeError("Database error")

        # Act & Assert
        with pytest.raises(RuntimeError, match="Database error"):
            use_case.execute()

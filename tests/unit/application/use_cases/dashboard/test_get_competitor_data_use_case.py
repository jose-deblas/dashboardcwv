"""
Unit tests for GetCompetitorDataUseCase.
"""

from datetime import date
from unittest.mock import Mock

import pytest

from src.application.dto.dashboard_dtos import FilterCriteria
from src.application.use_cases.dashboard.get_competitor_data_use_case import (
    GetCompetitorDataUseCase,
)
from src.domain.repositories.brand_repository import BrandRepository
from src.domain.repositories.dashboard_repository import DashboardRepository


class TestGetCompetitorDataUseCase:
    """Test suite for GetCompetitorDataUseCase."""

    @pytest.fixture
    def mock_repository(self) -> Mock:
        """Create a mock dashboard repository."""
        return Mock(spec=DashboardRepository)

    @pytest.fixture
    def mock_brand_repository(self) -> Mock:
        """Create a mock brand repository."""
        mock = Mock(spec=BrandRepository)
        # Mock target brands to return supermarket brands
        mock.get_target_brands.return_value = ["Lidl", "Mercadona"]
        return mock

    @pytest.fixture
    def use_case(
        self, mock_repository: Mock, mock_brand_repository: Mock
    ) -> GetCompetitorDataUseCase:
        """Create use case with mocked repositories."""
        return GetCompetitorDataUseCase(
            dashboard_repository=mock_repository,
            brand_repository=mock_brand_repository,
        )

    @pytest.fixture
    def filter_criteria(self) -> FilterCriteria:
        """Create sample filter criteria."""
        return FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            brands=None,
            countries=["ES"],
            page_types=None,
        )

    def test_execute_returns_competitor_data(
        self,
        use_case: GetCompetitorDataUseCase,
        mock_repository: Mock,
        filter_criteria: FilterCriteria,
    ):
        """Test that execute returns CompetitorData with rankings and time series."""
        # Arrange
        mock_rankings = [
            {"brand": "Lidl", "avg_performance_score": 95.0, "rank": 1},
            {"brand": "Caprabo", "avg_performance_score": 92.0, "rank": 2},
            {"brand": "Mercadona", "avg_performance_score": 90.0, "rank": 3},
        ]

        mock_time_series = [
            {
                "execution_date": date(2024, 1, 1),
                "brand": "Lidl",
                "avg_performance_score": 94.0,
            },
            {
                "execution_date": date(2024, 1, 1),
                "brand": "Caprabo",
                "avg_performance_score": 91.0,
            },
        ]

        mock_repository.get_brand_rankings.return_value = mock_rankings
        mock_repository.get_brand_time_series.return_value = mock_time_series

        # Act
        result = use_case.execute(filter_criteria, "mobile")

        # Assert
        assert result.device == "mobile"
        assert len(result.rankings) == 3

        # Check first ranking
        assert result.rankings[0].brand == "Lidl"
        assert result.rankings[0].avg_performance_score == 95.0
        assert result.rankings[0].rank == 1
        assert result.rankings[0].is_target_brand is True

        # Check third ranking
        assert result.rankings[2].brand == "Mercadona"
        assert result.rankings[2].is_target_brand is True

        # Check second ranking
        assert result.rankings[1].brand == "Caprabo"
        assert result.rankings[1].is_target_brand is False

        # Check time series
        assert len(result.time_series) == 2
        assert result.time_series[0].brand == "Lidl"

        # Verify repository calls
        mock_repository.get_brand_rankings.assert_called_once_with(
            target_date=filter_criteria.end_date,
            device="mobile",
            countries=filter_criteria.countries,
            page_types=filter_criteria.page_types,
            limit=3,
        )

        mock_repository.get_brand_time_series.assert_called_once()

    def test_execute_validates_device(
        self, use_case: GetCompetitorDataUseCase, filter_criteria: FilterCriteria
    ):
        """Test that execute validates device parameter."""
        # Act & Assert
        with pytest.raises(ValueError, match="device must be 'mobile' or 'desktop'"):
            use_case.execute(filter_criteria, "invalid")

    def test_get_rankings_returns_only_rankings(
        self,
        use_case: GetCompetitorDataUseCase,
        mock_repository: Mock,
        filter_criteria: FilterCriteria,
    ):
        """Test that get_rankings returns only ranking data."""
        # Arrange
        mock_rankings = [
            {"brand": "Lidl", "avg_performance_score": 95.0, "rank": 1},
            {"brand": "Mercadona", "avg_performance_score": 90.0, "rank": 2},
        ]

        mock_repository.get_brand_rankings.return_value = mock_rankings

        # Act
        result = use_case.get_rankings(filter_criteria, "desktop")

        # Assert
        assert len(result) == 2
        assert result[0].brand == "Lidl"
        assert result[0].is_target_brand is True
        assert result[1].brand == "Mercadona"
        assert result[1].is_target_brand is True

        # Verify repository was called correctly
        mock_repository.get_brand_rankings.assert_called_once_with(
            target_date=filter_criteria.end_date,
            device="desktop",
            countries=filter_criteria.countries,
            page_types=filter_criteria.page_types,
            limit=3,
        )

    def test_get_rankings_validates_device(
        self, use_case: GetCompetitorDataUseCase, filter_criteria: FilterCriteria
    ):
        """Test that get_rankings validates device parameter."""
        # Act & Assert
        with pytest.raises(ValueError, match="device must be 'mobile' or 'desktop'"):
            use_case.get_rankings(filter_criteria, "tablet")

    def test_execute_handles_empty_rankings(
        self,
        use_case: GetCompetitorDataUseCase,
        mock_repository: Mock,
        filter_criteria: FilterCriteria,
    ):
        """Test that execute handles case when no rankings exist."""
        # Arrange
        mock_repository.get_brand_rankings.return_value = []
        mock_repository.get_brand_time_series.return_value = []

        # Act
        result = use_case.execute(filter_criteria, "mobile")

        # Assert
        assert len(result.rankings) == 0
        assert len(result.time_series) == 0

    def test_execute_propagates_repository_errors(
        self,
        use_case: GetCompetitorDataUseCase,
        mock_repository: Mock,
        filter_criteria: FilterCriteria,
    ):
        """Test that repository errors are propagated to caller."""
        # Arrange
        mock_repository.get_brand_rankings.side_effect = RuntimeError("Database error")

        # Act & Assert
        with pytest.raises(RuntimeError, match="Database error"):
            use_case.execute(filter_criteria, "mobile")

"""
Unit tests for GetPerformanceDataUseCase.
"""

from datetime import date
from unittest.mock import Mock

import pytest

from src.application.dto.dashboard_dtos import FilterCriteria
from src.application.use_cases.dashboard.get_performance_data_use_case import (
    GetPerformanceDataUseCase,
)
from src.domain.repositories.dashboard_repository import DashboardRepository


class TestGetPerformanceDataUseCase:
    """Test suite for GetPerformanceDataUseCase."""

    @pytest.fixture
    def mock_repository(self) -> Mock:
        """Create a mock dashboard repository."""
        return Mock(spec=DashboardRepository)

    @pytest.fixture
    def use_case(self, mock_repository: Mock) -> GetPerformanceDataUseCase:
        """Create use case with mocked repository."""
        return GetPerformanceDataUseCase(dashboard_repository=mock_repository)

    @pytest.fixture
    def filter_criteria(self) -> FilterCriteria:
        """Create sample filter criteria."""
        return FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            brands=["Condis"],
            countries=["ES"],
            page_types=["home"],
        )

    def test_execute_returns_performance_metrics(
        self,
        use_case: GetPerformanceDataUseCase,
        mock_repository: Mock,
        filter_criteria: FilterCriteria,
    ):
        """Test that execute returns PerformanceMetrics with device data."""
        # Arrange
        mock_repository.get_performance_metrics_by_date.side_effect = [
            85.5,  # mobile start
            87.2,  # mobile end
            90.1,  # desktop start
            91.8,  # desktop end
        ]

        # Act
        result = use_case.execute(filter_criteria)

        # Assert
        assert result.mobile_metrics.device == "mobile"
        assert result.mobile_metrics.start_score == 85.5
        assert result.mobile_metrics.end_score == 87.2
        assert result.mobile_metrics.delta == pytest.approx(1.7, rel=0.01)
        assert result.mobile_metrics.traffic_light == "green"

        assert result.desktop_metrics.device == "desktop"
        assert result.desktop_metrics.start_score == 90.1
        assert result.desktop_metrics.end_score == 91.8
        assert result.desktop_metrics.delta == pytest.approx(1.7, rel=0.01)
        assert result.desktop_metrics.traffic_light == "green"

        # Verify repository was called correctly
        assert mock_repository.get_performance_metrics_by_date.call_count == 4

    def test_execute_handles_missing_data(
        self,
        use_case: GetPerformanceDataUseCase,
        mock_repository: Mock,
        filter_criteria: FilterCriteria,
    ):
        """Test that execute handles case when data is missing."""
        # Arrange
        mock_repository.get_performance_metrics_by_date.return_value = None

        # Act
        result = use_case.execute(filter_criteria)

        # Assert
        assert result.mobile_metrics.start_score is None
        assert result.mobile_metrics.end_score is None
        assert result.mobile_metrics.delta is None
        assert result.mobile_metrics.traffic_light == "amber"

    def test_execute_handles_negative_delta(
        self,
        use_case: GetPerformanceDataUseCase,
        mock_repository: Mock,
        filter_criteria: FilterCriteria,
    ):
        """Test traffic light is red when performance declines."""
        # Arrange
        mock_repository.get_performance_metrics_by_date.side_effect = [
            90.0,  # mobile start
            85.0,  # mobile end (decline)
            95.0,  # desktop start
            95.0,  # desktop end (no change)
        ]

        # Act
        result = use_case.execute(filter_criteria)

        # Assert
        assert result.mobile_metrics.delta == pytest.approx(-5.0, rel=0.01)
        assert result.mobile_metrics.traffic_light == "red"
        assert result.desktop_metrics.delta == pytest.approx(0.0, rel=0.01)
        assert result.desktop_metrics.traffic_light == "amber"

    def test_get_time_series_returns_data(
        self,
        use_case: GetPerformanceDataUseCase,
        mock_repository: Mock,
        filter_criteria: FilterCriteria,
    ):
        """Test that get_time_series returns time series points."""
        # Arrange
        mock_repository.get_performance_time_series.return_value = [
            {"execution_date": date(2024, 1, 1), "avg_performance_score": 85.5},
            {"execution_date": date(2024, 1, 2), "avg_performance_score": 86.0},
        ]

        # Act
        result = use_case.get_time_series(filter_criteria, "mobile")

        # Assert
        assert len(result) == 2
        assert result[0].execution_date == date(2024, 1, 1)
        assert result[0].avg_performance_score == 85.5
        assert result[1].execution_date == date(2024, 1, 2)
        assert result[1].avg_performance_score == 86.0

        # Verify repository was called correctly
        mock_repository.get_performance_time_series.assert_called_once_with(
            start_date=filter_criteria.start_date,
            end_date=filter_criteria.end_date,
            device="mobile",
            brands=filter_criteria.brands,
            countries=filter_criteria.countries,
            page_types=filter_criteria.page_types,
        )

    def test_get_time_series_validates_device(
        self,
        use_case: GetPerformanceDataUseCase,
        filter_criteria: FilterCriteria,
    ):
        """Test that get_time_series validates device parameter."""
        # Act & Assert
        with pytest.raises(ValueError, match="device must be 'mobile' or 'desktop'"):
            use_case.get_time_series(filter_criteria, "invalid")

    def test_execute_propagates_repository_errors(
        self,
        use_case: GetPerformanceDataUseCase,
        mock_repository: Mock,
        filter_criteria: FilterCriteria,
    ):
        """Test that repository errors are propagated to caller."""
        # Arrange
        mock_repository.get_performance_metrics_by_date.side_effect = RuntimeError(
            "Database error"
        )

        # Act & Assert
        with pytest.raises(RuntimeError, match="Database error"):
            use_case.execute(filter_criteria)

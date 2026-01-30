"""
Tests for dashboard DTOs.

Note: Calculation logic (delta, growth_rate, colors, formatting) has been moved
to presentation layer presenters. See:
- tests/unit/presentation/presenters/test_performance_presenter.py for calculations
- tests/unit/presentation/presenters/test_competitor_presenter.py for rankings
- tests/unit/presentation/presenters/test_filter_presenter.py for filters

DTOs are now pure data containers with no presentation logic.
"""

from datetime import date

import pytest

from src.application.dto.dashboard_dtos import (
    DeviceMetrics,
    PerformanceMetrics,
    TimeSeriesPoint,
    FilterCriteria,
    FilterOptions,
    BrandRanking,
    CompetitorData,
)


class TestDeviceMetrics:
    """Test DeviceMetrics DTO."""

    def test_create_with_all_scores(self):
        """Test creating DeviceMetrics with all scores."""
        dm = DeviceMetrics(device="mobile", start_score=50.0, end_score=60.0)

        assert dm.device == "mobile"
        assert dm.start_score == 50.0
        assert dm.end_score == 60.0

    def test_create_with_none_start_score(self):
        """Test creating DeviceMetrics with None start_score."""
        dm = DeviceMetrics(device="mobile", start_score=None, end_score=60.0)

        assert dm.device == "mobile"
        assert dm.start_score is None
        assert dm.end_score == 60.0

    def test_create_with_none_end_score(self):
        """Test creating DeviceMetrics with None end_score."""
        dm = DeviceMetrics(device="desktop", start_score=70.0, end_score=None)

        assert dm.device == "desktop"
        assert dm.start_score == 70.0
        assert dm.end_score is None

    def test_create_with_all_none_scores(self):
        """Test creating DeviceMetrics with all None scores."""
        dm = DeviceMetrics(device="mobile", start_score=None, end_score=None)

        assert dm.device == "mobile"
        assert dm.start_score is None
        assert dm.end_score is None

    def test_immutability(self):
        """Test that DeviceMetrics is immutable (frozen dataclass)."""
        dm = DeviceMetrics(device="mobile", start_score=50.0, end_score=60.0)

        with pytest.raises(Exception):  # FrozenInstanceError
            dm.device = "desktop"


class TestPerformanceMetrics:
    """Test PerformanceMetrics DTO."""

    def test_create_complete(self):
        """Test creating PerformanceMetrics with all data."""
        mobile = DeviceMetrics(device="mobile", start_score=50.0, end_score=60.0)
        desktop = DeviceMetrics(device="desktop", start_score=70.0, end_score=75.0)
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        pm = PerformanceMetrics(
            mobile_metrics=mobile, desktop_metrics=desktop, filter_criteria=criteria
        )

        assert pm.mobile_metrics == mobile
        assert pm.desktop_metrics == desktop
        assert pm.filter_criteria == criteria


class TestTimeSeriesPoint:
    """Test TimeSeriesPoint DTO."""

    def test_create(self):
        """Test creating TimeSeriesPoint."""
        ts = TimeSeriesPoint(execution_date=date(2024, 1, 1), avg_performance_score=50.0)

        assert ts.execution_date == date(2024, 1, 1)
        assert ts.avg_performance_score == 50.0

    def test_immutability(self):
        """Test that TimeSeriesPoint is immutable."""
        ts = TimeSeriesPoint(execution_date=date(2024, 1, 1), avg_performance_score=50.0)

        with pytest.raises(Exception):
            ts.avg_performance_score = 60.0


class TestFilterCriteria:
    """Test FilterCriteria DTO."""

    def test_create_with_all_fields(self):
        """Test creating FilterCriteria with all fields."""
        fc = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A", "Brand B"],
            countries=["US", "UK"],
            page_types=["home", "product"],
        )

        assert fc.start_date == date(2024, 1, 1)
        assert fc.end_date == date(2024, 1, 31)
        assert fc.brands == ["Brand A", "Brand B"]
        assert fc.countries == ["US", "UK"]
        assert fc.page_types == ["home", "product"]

    def test_create_with_none_optional_fields(self):
        """Test creating FilterCriteria with None optional fields."""
        fc = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=None,
            countries=None,
            page_types=None,
        )

        assert fc.brands is None
        assert fc.countries is None
        assert fc.page_types is None

    def test_immutability(self):
        """Test that FilterCriteria is immutable."""
        fc = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        with pytest.raises(Exception):
            fc.brands = ["Brand B"]

    # Note: Date validation has been moved to FilterValidator
    # See tests/unit/application/validation/test_filter_validator.py


class TestFilterOptions:
    """Test FilterOptions DTO."""

    def test_create_complete(self):
        """Test creating FilterOptions with all fields."""
        fo = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=["Brand A", "Brand B"],
            countries=["US", "UK"],
            page_types=["home", "product"],
        )

        assert fo.min_date == date(2024, 1, 1)
        assert fo.max_date == date(2024, 12, 31)
        assert len(fo.brands) == 2
        assert len(fo.countries) == 2
        assert len(fo.page_types) == 2

    def test_immutability(self):
        """Test that FilterOptions is immutable."""
        fo = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        with pytest.raises(Exception):
            fo.brands = ["Brand B"]


class TestBrandRanking:
    """Test BrandRanking DTO."""

    def test_create_with_all_fields(self):
        """Test creating BrandRanking."""
        br = BrandRanking(
            rank=1, brand="Brand A", avg_performance_score=85.5, is_target_brand=True
        )

        assert br.rank == 1
        assert br.brand == "Brand A"
        assert br.avg_performance_score == 85.5
        assert br.is_target_brand is True

    def test_create_non_target_brand(self):
        """Test creating BrandRanking for non-target brand."""
        br = BrandRanking(
            rank=5, brand="Competitor", avg_performance_score=70.0, is_target_brand=False
        )

        assert br.rank == 5
        assert br.is_target_brand is False

    def test_immutability(self):
        """Test that BrandRanking is immutable."""
        br = BrandRanking(
            rank=1, brand="Brand A", avg_performance_score=85.5, is_target_brand=True
        )

        with pytest.raises(Exception):
            br.rank = 2

    # Note: Medal assignment and highlighting logic has been moved to CompetitorPresenter
    # See tests/unit/presentation/presenters/test_competitor_presenter.py


class TestCompetitorData:
    """Test CompetitorData DTO."""

    def test_create_complete(self):
        """Test creating CompetitorData with all fields."""
        rankings = [
            BrandRanking(
                rank=1, brand="Brand A", avg_performance_score=85.0, is_target_brand=False
            ),
            BrandRanking(
                rank=2, brand="Brand B", avg_performance_score=80.0, is_target_brand=True
            ),
        ]

        time_series = [
            TimeSeriesPoint(execution_date=date(2024, 1, 1), avg_performance_score=80.0),
            TimeSeriesPoint(execution_date=date(2024, 1, 31), avg_performance_score=85.0),
        ]

        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A", "Brand B"],
            countries=["US"],
            page_types=["home"],
        )

        cd = CompetitorData(
            device="mobile",
            rankings=rankings,
            time_series=time_series,
            filter_criteria=criteria,
        )

        assert len(cd.rankings) == 2
        assert len(cd.time_series) == 2
        assert cd.filter_criteria == criteria

    def test_create_with_empty_time_series(self):
        """Test creating CompetitorData with empty time series."""
        rankings = [
            BrandRanking(
                rank=1, brand="Brand A", avg_performance_score=85.0, is_target_brand=True
            ),
        ]

        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        cd = CompetitorData(
            device="mobile", rankings=rankings, time_series=[], filter_criteria=criteria
        )

        assert len(cd.rankings) == 1
        assert len(cd.time_series) == 0


class TestDTOIntegration:
    """Integration tests for DTOs working together."""

    def test_complete_performance_metrics_structure(self):
        """Test creating complete PerformanceMetrics structure."""
        mobile = DeviceMetrics(device="mobile", start_score=50.0, end_score=60.0)
        desktop = DeviceMetrics(device="desktop", start_score=70.0, end_score=75.0)

        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        pm = PerformanceMetrics(
            mobile_metrics=mobile, desktop_metrics=desktop, filter_criteria=criteria
        )

        # Verify structure
        assert pm.mobile_metrics.device == "mobile"
        assert pm.desktop_metrics.device == "desktop"
        assert pm.filter_criteria.brands == ["Brand A"]

    def test_complete_competitor_data_structure(self):
        """Test creating complete CompetitorData structure."""
        rankings = [
            BrandRanking(
                rank=1, brand="Brand A", avg_performance_score=85.0, is_target_brand=False
            ),
            BrandRanking(
                rank=2, brand="Our Brand", avg_performance_score=80.0, is_target_brand=True
            ),
            BrandRanking(
                rank=3, brand="Brand C", avg_performance_score=75.0, is_target_brand=False
            ),
        ]

        time_series = [
            TimeSeriesPoint(execution_date=date(2024, 1, 1), avg_performance_score=78.0),
            TimeSeriesPoint(execution_date=date(2024, 1, 15), avg_performance_score=79.0),
            TimeSeriesPoint(execution_date=date(2024, 1, 31), avg_performance_score=80.0),
        ]

        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A", "Our Brand", "Brand C"],
            countries=None,
            page_types=None,
        )

        cd = CompetitorData(
            device="mobile",
            rankings=rankings,
            time_series=time_series,
            filter_criteria=criteria,
        )

        # Verify structure
        assert len(cd.rankings) == 3
        assert cd.rankings[1].is_target_brand is True
        assert len(cd.time_series) == 3
        assert cd.filter_criteria.countries is None

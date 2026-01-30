"""
Tests for CompetitorPresenter.

Tests presentation logic for competitor rankings:
- Medal assignment (🥇🥈🥉)
- Highlighting target brands
- Score formatting
"""

from datetime import date

import pytest

from src.application.dto.dashboard_dtos import (
    CompetitorData,
    BrandRanking,
    FilterCriteria,
    TimeSeriesPoint,
)
from src.presentation.presenters.competitor_presenter import CompetitorPresenter
from src.presentation.models.competitor_view_model import (
    CompetitorViewModel,
    RankingViewModel,
)


class TestCompetitorPresenter:
    """Test suite for CompetitorPresenter."""

    @pytest.fixture
    def presenter(self):
        """Create presenter instance."""
        return CompetitorPresenter()

    @pytest.fixture
    def filter_criteria(self):
        """Create sample filter criteria."""
        return FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A", "Brand B"],
            countries=["US"],
            page_types=["home"],
        )

    # Test _present_ranking - Medal assignment
    def test_ranking_first_place_gets_gold_medal(self, presenter):
        """Test that rank 1 gets gold medal."""
        ranking = BrandRanking(
            rank=1, brand="Brand A", avg_performance_score=85.5, is_target_brand=False
        )

        result = presenter._present_ranking(ranking)

        assert result.medal == "🥇"
        assert result.rank == 1

    def test_ranking_second_place_gets_silver_medal(self, presenter):
        """Test that rank 2 gets silver medal."""
        ranking = BrandRanking(
            rank=2, brand="Brand B", avg_performance_score=80.0, is_target_brand=False
        )

        result = presenter._present_ranking(ranking)

        assert result.medal == "🥈"
        assert result.rank == 2

    def test_ranking_third_place_gets_bronze_medal(self, presenter):
        """Test that rank 3 gets bronze medal."""
        ranking = BrandRanking(
            rank=3, brand="Brand C", avg_performance_score=75.0, is_target_brand=False
        )

        result = presenter._present_ranking(ranking)

        assert result.medal == "🥉"
        assert result.rank == 3

    def test_ranking_fourth_place_no_medal(self, presenter):
        """Test that rank 4 and beyond get no medal."""
        ranking = BrandRanking(
            rank=4, brand="Brand D", avg_performance_score=70.0, is_target_brand=False
        )

        result = presenter._present_ranking(ranking)

        assert result.medal == ""
        assert result.rank == 4

    def test_ranking_tenth_place_no_medal(self, presenter):
        """Test that rank 10 gets no medal."""
        ranking = BrandRanking(
            rank=10, brand="Brand J", avg_performance_score=50.0, is_target_brand=False
        )

        result = presenter._present_ranking(ranking)

        assert result.medal == ""
        assert result.rank == 10

    # Test _present_ranking - Score formatting
    def test_ranking_score_formatted_two_decimals(self, presenter):
        """Test score is formatted to 2 decimal places."""
        ranking = BrandRanking(
            rank=1, brand="Brand A", avg_performance_score=85.12345, is_target_brand=False
        )

        result = presenter._present_ranking(ranking)

        assert result.score == "85.12"

    def test_ranking_score_formatted_integer(self, presenter):
        """Test integer score is formatted with decimals."""
        ranking = BrandRanking(
            rank=1, brand="Brand A", avg_performance_score=75.0, is_target_brand=False
        )

        result = presenter._present_ranking(ranking)

        assert result.score == "75.00"

    def test_ranking_score_formatted_small_value(self, presenter):
        """Test small score values are formatted correctly."""
        ranking = BrandRanking(
            rank=5, brand="Brand E", avg_performance_score=12.5, is_target_brand=False
        )

        result = presenter._present_ranking(ranking)

        assert result.score == "12.50"

    # Test _present_ranking - Highlighting
    def test_ranking_target_brand_is_highlighted(self, presenter):
        """Test target brand is marked as highlighted."""
        ranking = BrandRanking(
            rank=2, brand="Our Brand", avg_performance_score=80.0, is_target_brand=True
        )

        result = presenter._present_ranking(ranking)

        assert result.is_highlighted is True
        assert result.brand == "Our Brand"

    def test_ranking_non_target_brand_not_highlighted(self, presenter):
        """Test non-target brand is not highlighted."""
        ranking = BrandRanking(
            rank=1,
            brand="Competitor",
            avg_performance_score=85.0,
            is_target_brand=False,
        )

        result = presenter._present_ranking(ranking)

        assert result.is_highlighted is False

    def test_ranking_target_brand_with_medal(self, presenter):
        """Test target brand that also has a medal."""
        ranking = BrandRanking(
            rank=1, brand="Our Brand", avg_performance_score=90.0, is_target_brand=True
        )

        result = presenter._present_ranking(ranking)

        assert result.medal == "🥇"
        assert result.is_highlighted is True

    # Test _present_ranking - Complete transformation
    def test_ranking_complete_transformation(self, presenter):
        """Test complete ranking transformation."""
        ranking = BrandRanking(
            rank=2, brand="Brand B", avg_performance_score=78.567, is_target_brand=True
        )

        result = presenter._present_ranking(ranking)

        assert isinstance(result, RankingViewModel)
        assert result.rank == 2
        assert result.brand == "Brand B"
        assert result.score == "78.57"
        assert result.medal == "🥈"
        assert result.is_highlighted is True

    # Test present() - Main entry point
    def test_present_complete(self, presenter, filter_criteria):
        """Test complete presentation transformation."""
        mobile_data = CompetitorData(
            device="mobile",
            rankings=[
                BrandRanking(
                    rank=1, brand="Brand A", avg_performance_score=85.0, is_target_brand=False
                ),
                BrandRanking(
                    rank=2, brand="Brand B", avg_performance_score=80.0, is_target_brand=True
                ),
                BrandRanking(
                    rank=3, brand="Brand C", avg_performance_score=75.0, is_target_brand=False
                ),
            ],
            time_series=[
                TimeSeriesPoint(execution_date=date(2024, 1, 1), avg_performance_score=80.0),
            ],
            filter_criteria=filter_criteria,
        )

        desktop_data = CompetitorData(
            device="desktop",
            rankings=[
                BrandRanking(
                    rank=1, brand="Brand X", avg_performance_score=90.0, is_target_brand=True
                ),
                BrandRanking(
                    rank=2, brand="Brand Y", avg_performance_score=85.0, is_target_brand=False
                ),
            ],
            time_series=[
                TimeSeriesPoint(execution_date=date(2024, 1, 1), avg_performance_score=90.0),
            ],
            filter_criteria=filter_criteria,
        )

        result = presenter.present(mobile_data, desktop_data)

        # Check instance type
        assert isinstance(result, CompetitorViewModel)

        # Check mobile rankings
        assert len(result.mobile_rankings) == 3
        assert result.mobile_rankings[0].medal == "🥇"
        assert result.mobile_rankings[1].medal == "🥈"
        assert result.mobile_rankings[1].is_highlighted is True
        assert result.mobile_rankings[2].medal == "🥉"

        # Check desktop rankings
        assert len(result.desktop_rankings) == 2
        assert result.desktop_rankings[0].medal == "🥇"
        assert result.desktop_rankings[0].is_highlighted is True
        assert result.desktop_rankings[1].medal == "🥈"

        # Check time series flags
        assert result.has_mobile_time_series is True
        assert result.has_desktop_time_series is True

        # Check active filters
        assert len(result.active_filters_display) == 4

    def test_present_no_time_series(self, presenter, filter_criteria):
        """Test presentation with no time series data."""
        mobile_data = CompetitorData(
            device="mobile",
            rankings=[
                BrandRanking(
                    rank=1, brand="Brand A", avg_performance_score=85.0, is_target_brand=False
                ),
            ],
            time_series=[],
            filter_criteria=filter_criteria,
        )

        desktop_data = CompetitorData(
            device="desktop",
            rankings=[
                BrandRanking(
                    rank=1, brand="Brand X", avg_performance_score=90.0, is_target_brand=False
                ),
            ],
            time_series=[],
            filter_criteria=filter_criteria,
        )

        result = presenter.present(mobile_data, desktop_data)

        assert result.has_mobile_time_series is False
        assert result.has_desktop_time_series is False

    def test_present_empty_rankings(self, presenter, filter_criteria):
        """Test presentation with empty rankings."""
        mobile_data = CompetitorData(
            device="mobile",
            rankings=[],
            time_series=[],
            filter_criteria=filter_criteria,
        )

        desktop_data = CompetitorData(
            device="desktop",
            rankings=[],
            time_series=[],
            filter_criteria=filter_criteria,
        )

        result = presenter.present(mobile_data, desktop_data)

        assert len(result.mobile_rankings) == 0
        assert len(result.desktop_rankings) == 0
        assert result.has_mobile_time_series is False
        assert result.has_desktop_time_series is False

    def test_present_only_mobile_time_series(self, presenter, filter_criteria):
        """Test presentation with only mobile time series."""
        mobile_data = CompetitorData(
            device="mobile",
            rankings=[
                BrandRanking(
                    rank=1, brand="Brand A", avg_performance_score=85.0, is_target_brand=False
                ),
            ],
            time_series=[
                TimeSeriesPoint(execution_date=date(2024, 1, 1), avg_performance_score=85.0),
            ],
            filter_criteria=filter_criteria,
        )

        desktop_data = CompetitorData(
            device="desktop",
            rankings=[
                BrandRanking(
                    rank=1, brand="Brand X", avg_performance_score=90.0, is_target_brand=False
                ),
            ],
            time_series=[],
            filter_criteria=filter_criteria,
        )

        result = presenter.present(mobile_data, desktop_data)

        assert result.has_mobile_time_series is True
        assert result.has_desktop_time_series is False

    # Test _format_active_filters
    def test_format_active_filters_all_specified(self, presenter):
        """Test filter formatting with all values specified."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A", "Brand B", "Brand C"],
            countries=["US", "UK", "CA"],
            page_types=["home", "product", "category"],
        )

        result = presenter._format_active_filters(criteria)

        assert len(result) == 4
        assert result[0] == "From 2024-01-01 to 2024-01-31"
        assert result[1] == "Brand: Brand A, Brand B, Brand C"
        assert result[2] == "Country: US, UK, CA"
        assert result[3] == "Page Types: home, product, category"

    def test_format_active_filters_none_values(self, presenter):
        """Test filter formatting with None values."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=None,
            countries=None,
            page_types=None,
        )

        result = presenter._format_active_filters(criteria)

        assert len(result) == 4
        assert result[0] == "From 2024-01-01 to 2024-01-31"
        assert result[1] == "Brand: All Brands"
        assert result[2] == "Country: All Countries"
        assert result[3] == "Page Types: All Page Types"


class TestCompetitorPresenterEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def presenter(self):
        """Create presenter instance."""
        return CompetitorPresenter()

    @pytest.fixture
    def filter_criteria(self):
        """Create sample filter criteria."""
        return FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A", "Brand B"],
            countries=["US"],
            page_types=["home"],
        )

    def test_ranking_with_zero_score(self, presenter):
        """Test ranking with zero score."""
        ranking = BrandRanking(
            rank=5, brand="Brand E", avg_performance_score=0.0, is_target_brand=False
        )

        result = presenter._present_ranking(ranking)

        assert result.score == "0.00"
        assert result.medal == ""

    def test_ranking_with_perfect_score(self, presenter):
        """Test ranking with perfect 100 score."""
        ranking = BrandRanking(
            rank=1, brand="Brand A", avg_performance_score=100.0, is_target_brand=True
        )

        result = presenter._present_ranking(ranking)

        assert result.score == "100.00"
        assert result.medal == "🥇"
        assert result.is_highlighted is True

    def test_ranking_with_very_low_score(self, presenter):
        """Test ranking with very low score."""
        ranking = BrandRanking(
            rank=10, brand="Brand J", avg_performance_score=5.25, is_target_brand=False
        )

        result = presenter._present_ranking(ranking)

        assert result.score == "5.25"

    def test_multiple_target_brands(self, presenter, filter_criteria):
        """Test presentation with multiple target brands."""
        mobile_data = CompetitorData(
            device="mobile",
            rankings=[
                BrandRanking(
                    rank=1, brand="Our Brand 1", avg_performance_score=85.0, is_target_brand=True
                ),
                BrandRanking(
                    rank=2, brand="Competitor", avg_performance_score=80.0, is_target_brand=False
                ),
                BrandRanking(
                    rank=3, brand="Our Brand 2", avg_performance_score=75.0, is_target_brand=True
                ),
            ],
            time_series=[],
            filter_criteria=filter_criteria,
        )

        desktop_data = CompetitorData(
            device="desktop",
            rankings=[],
            time_series=[],
            filter_criteria=filter_criteria,
        )

        result = presenter.present(mobile_data, desktop_data)

        # Both target brands should be highlighted
        assert result.mobile_rankings[0].is_highlighted is True
        assert result.mobile_rankings[1].is_highlighted is False
        assert result.mobile_rankings[2].is_highlighted is True

    def test_single_brand_in_rankings(self, presenter, filter_criteria):
        """Test presentation with only one brand."""
        mobile_data = CompetitorData(
            device="mobile",
            rankings=[
                BrandRanking(
                    rank=1, brand="Only Brand", avg_performance_score=75.0, is_target_brand=True
                ),
            ],
            time_series=[],
            filter_criteria=filter_criteria,
        )

        desktop_data = CompetitorData(
            device="desktop",
            rankings=[
                BrandRanking(
                    rank=1, brand="Only Brand", avg_performance_score=80.0, is_target_brand=True
                ),
            ],
            time_series=[],
            filter_criteria=filter_criteria,
        )

        result = presenter.present(mobile_data, desktop_data)

        assert len(result.mobile_rankings) == 1
        assert result.mobile_rankings[0].medal == "🥇"
        assert result.mobile_rankings[0].is_highlighted is True

        assert len(result.desktop_rankings) == 1
        assert result.desktop_rankings[0].medal == "🥇"

    def test_floating_point_precision_in_scores(self, presenter):
        """Test floating point precision in score formatting."""
        ranking = BrandRanking(
            rank=1, brand="Brand A", avg_performance_score=33.33333, is_target_brand=False
        )

        result = presenter._present_ranking(ranking)

        assert result.score == "33.33"

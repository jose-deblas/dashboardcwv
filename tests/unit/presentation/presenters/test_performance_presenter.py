"""
Tests for PerformancePresenter.

Tests all calculation logic that was moved from DeviceMetrics DTO:
- Delta calculations
- Growth rate calculations
- Color determination
- Value formatting
- Target values
- Edge cases
"""

from datetime import date
from typing import Optional

import pytest

from src.application.dto.dashboard_dtos import (
    DeviceMetrics,
    PerformanceMetrics,
    TimeSeriesPoint,
    FilterCriteria,
)
from src.presentation.presenters.performance_presenter import PerformancePresenter
from src.presentation.models.performance_view_model import (
    PerformanceViewModel,
    DeviceMetricsViewModel,
    MetricCardViewModel,
)


class TestPerformancePresenter:
    """Test suite for PerformancePresenter."""

    @pytest.fixture
    def presenter(self):
        """Create presenter instance."""
        return PerformancePresenter()

    @pytest.fixture
    def filter_criteria(self):
        """Create sample filter criteria."""
        return FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A", "Brand B"],
            countries=["US"],
            page_types=["home", "product"],
        )

    # Test _format_score
    def test_format_score_with_value(self, presenter):
        """Test score formatting with valid value."""
        result = presenter._format_score(65.12345)
        assert result == "65.12"

    def test_format_score_with_none(self, presenter):
        """Test score formatting with None returns N/A."""
        result = presenter._format_score(None)
        assert result == "N/A"

    def test_format_score_with_zero(self, presenter):
        """Test score formatting with zero."""
        result = presenter._format_score(0.0)
        assert result == "0.00"

    # Test _format_delta
    def test_format_delta_positive(self, presenter):
        """Test delta formatting with positive value includes + sign."""
        result = presenter._format_delta(5.2)
        assert result == "+5.20"

    def test_format_delta_negative(self, presenter):
        """Test delta formatting with negative value includes - sign."""
        result = presenter._format_delta(-3.45)
        assert result == "-3.45"

    def test_format_delta_zero(self, presenter):
        """Test delta formatting with zero has no sign."""
        result = presenter._format_delta(0.0)
        assert result == "0.00"

    def test_format_delta_none(self, presenter):
        """Test delta formatting with None returns None."""
        result = presenter._format_delta(None)
        assert result is None

    # Test _format_growth_rate
    def test_format_growth_rate_positive(self, presenter):
        """Test growth rate formatting with positive value."""
        result = presenter._format_growth_rate(12.34)
        assert result == "+12.34%"

    def test_format_growth_rate_negative(self, presenter):
        """Test growth rate formatting with negative value."""
        result = presenter._format_growth_rate(-8.76)
        assert result == "-8.76%"

    def test_format_growth_rate_zero(self, presenter):
        """Test growth rate formatting with zero."""
        result = presenter._format_growth_rate(0.0)
        assert result == "0.00%"

    def test_format_growth_rate_none(self, presenter):
        """Test growth rate formatting with None returns N/A."""
        result = presenter._format_growth_rate(None)
        assert result == "N/A"

    # Test _get_delta_color
    def test_delta_color_positive(self, presenter):
        """Test positive delta returns green."""
        result = presenter._get_delta_color(5.0)
        assert result == "green"

    def test_delta_color_negative(self, presenter):
        """Test negative delta returns red."""
        result = presenter._get_delta_color(-3.0)
        assert result == "red"

    def test_delta_color_zero(self, presenter):
        """Test zero delta returns neutral."""
        result = presenter._get_delta_color(0.0)
        assert result == "neutral"

    def test_delta_color_none(self, presenter):
        """Test None delta returns neutral."""
        result = presenter._get_delta_color(None)
        assert result == "neutral"

    # Test _get_growth_color
    def test_growth_color_positive(self, presenter):
        """Test positive growth rate returns green."""
        result = presenter._get_growth_color(10.0)
        assert result == "green"

    def test_growth_color_negative(self, presenter):
        """Test negative growth rate returns red."""
        result = presenter._get_growth_color(-5.0)
        assert result == "red"

    def test_growth_color_zero(self, presenter):
        """Test zero growth rate returns neutral."""
        result = presenter._get_growth_color(0.0)
        assert result == "neutral"

    def test_growth_color_none(self, presenter):
        """Test None growth rate returns neutral."""
        result = presenter._get_growth_color(None)
        assert result == "neutral"

    # Test _present_device_metrics - Delta calculation
    def test_device_metrics_delta_positive(self, presenter):
        """Test delta calculation with positive change."""
        metrics = DeviceMetrics(device="mobile", start_score=50.0, end_score=60.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        assert result.end_date_card.delta == "+10.00"
        assert result.end_date_card.delta_color == "green"

    def test_device_metrics_delta_negative(self, presenter):
        """Test delta calculation with negative change."""
        metrics = DeviceMetrics(device="mobile", start_score=60.0, end_score=55.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        assert result.end_date_card.delta == "-5.00"
        assert result.end_date_card.delta_color == "red"

    def test_device_metrics_delta_zero(self, presenter):
        """Test delta calculation with no change."""
        metrics = DeviceMetrics(device="mobile", start_score=50.0, end_score=50.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        assert result.end_date_card.delta == "0.00"
        assert result.end_date_card.delta_color == "neutral"

    # Test _present_device_metrics - Growth rate calculation
    def test_device_metrics_growth_rate_positive(self, presenter):
        """Test growth rate calculation with positive growth."""
        metrics = DeviceMetrics(device="mobile", start_score=50.0, end_score=60.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        # (60 - 50) / 50 * 100 = 20%
        assert result.growth_rate_display == "+20.00%"
        assert result.growth_rate_color == "green"

    def test_device_metrics_growth_rate_negative(self, presenter):
        """Test growth rate calculation with negative growth."""
        metrics = DeviceMetrics(device="mobile", start_score=50.0, end_score=40.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        # (40 - 50) / 50 * 100 = -20%
        assert result.growth_rate_display == "-20.00%"
        assert result.growth_rate_color == "red"

    def test_device_metrics_growth_rate_fractional(self, presenter):
        """Test growth rate calculation with fractional percentage."""
        metrics = DeviceMetrics(device="mobile", start_score=60.0, end_score=65.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        # (65 - 60) / 60 * 100 = 8.33%
        assert result.growth_rate_display == "+8.33%"
        assert result.growth_rate_color == "green"

    # Test _present_device_metrics - Edge cases with None
    def test_device_metrics_both_scores_none(self, presenter):
        """Test metrics with both scores None."""
        metrics = DeviceMetrics(device="mobile", start_score=None, end_score=None)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        assert result.has_data is False
        assert result.start_date_card.value == "N/A"
        assert result.end_date_card.value == "N/A"
        assert result.end_date_card.delta is None
        assert result.growth_rate_display == "N/A"

    def test_device_metrics_start_score_none(self, presenter):
        """Test metrics with start score None."""
        metrics = DeviceMetrics(device="mobile", start_score=None, end_score=60.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        assert result.has_data is True
        assert result.start_date_card.value == "N/A"
        assert result.end_date_card.value == "60.00"
        assert result.end_date_card.delta is None
        assert result.growth_rate_display == "N/A"

    def test_device_metrics_end_score_none(self, presenter):
        """Test metrics with end score None."""
        metrics = DeviceMetrics(device="mobile", start_score=50.0, end_score=None)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        assert result.has_data is True
        assert result.start_date_card.value == "50.00"
        assert result.end_date_card.value == "N/A"
        assert result.end_date_card.delta is None
        assert result.growth_rate_display == "N/A"

    # Test _present_device_metrics - Edge case with zero start score
    def test_device_metrics_zero_start_score(self, presenter):
        """Test growth rate with zero start score (division by zero)."""
        metrics = DeviceMetrics(device="mobile", start_score=0.0, end_score=10.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        # Should not crash, growth rate should be N/A
        assert result.growth_rate_display == "N/A"
        assert result.growth_rate_color == "neutral"
        # But delta should still work
        assert result.end_date_card.delta == "+10.00"

    # Test _present_device_metrics - Target values
    def test_device_metrics_mobile_target(self, presenter):
        """Test mobile target value is correctly set."""
        metrics = DeviceMetrics(device="mobile", start_score=50.0, end_score=60.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        assert result.target_card.label == "Target"
        assert result.target_card.value == "65.00"
        assert result.target_card.help_text == "Performance score target for mobile"

    def test_device_metrics_desktop_target(self, presenter):
        """Test desktop target value is correctly set."""
        metrics = DeviceMetrics(device="desktop", start_score=70.0, end_score=75.0)
        result = presenter._present_device_metrics(metrics, "Desktop", 80)

        assert result.target_card.label == "Target"
        assert result.target_card.value == "80.00"
        assert result.target_card.help_text == "Performance score target for desktop"

    # Test _present_device_metrics - Device labels
    def test_device_metrics_mobile_label(self, presenter):
        """Test mobile device label."""
        metrics = DeviceMetrics(device="mobile", start_score=50.0, end_score=60.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        assert result.device_label == "Mobile"

    def test_device_metrics_desktop_label(self, presenter):
        """Test desktop device label."""
        metrics = DeviceMetrics(device="desktop", start_score=70.0, end_score=75.0)
        result = presenter._present_device_metrics(metrics, "Desktop", 80)

        assert result.device_label == "Desktop"

    # Test _format_active_filters
    def test_format_active_filters_all_specified(self, presenter):
        """Test filter formatting with all values specified."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A", "Brand B"],
            countries=["US", "UK"],
            page_types=["home", "product"],
        )

        result = presenter._format_active_filters(criteria)

        assert len(result) == 4
        assert result[0] == "From 2024-01-01 to 2024-01-31"
        assert result[1] == "Brand: Brand A, Brand B"
        assert result[2] == "Country: US, UK"
        assert result[3] == "Page Types: home, product"

    def test_format_active_filters_none_brands(self, presenter):
        """Test filter formatting with no brands specified."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=None,
            countries=["US"],
            page_types=["home"],
        )

        result = presenter._format_active_filters(criteria)

        assert result[1] == "Brand: All Brands"

    def test_format_active_filters_none_countries(self, presenter):
        """Test filter formatting with no countries specified."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=None,
            page_types=["home"],
        )

        result = presenter._format_active_filters(criteria)

        assert result[2] == "Country: All Countries"

    def test_format_active_filters_none_page_types(self, presenter):
        """Test filter formatting with no page types specified."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=None,
        )

        result = presenter._format_active_filters(criteria)

        assert result[3] == "Page Types: All Page Types"

    def test_format_active_filters_all_none(self, presenter):
        """Test filter formatting with all optional values None."""
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

    # Test present() - Main entry point
    def test_present_complete(self, presenter, filter_criteria):
        """Test complete presentation transformation."""
        performance_metrics = PerformanceMetrics(
            mobile_metrics=DeviceMetrics(
                device="mobile", start_score=50.0, end_score=60.0
            ),
            desktop_metrics=DeviceMetrics(
                device="desktop", start_score=70.0, end_score=75.0
            ),
            filter_criteria=filter_criteria,
        )

        mobile_ts = [
            TimeSeriesPoint(execution_date=date(2024, 1, 1), avg_performance_score=50.0),
            TimeSeriesPoint(execution_date=date(2024, 1, 31), avg_performance_score=60.0),
        ]

        desktop_ts = [
            TimeSeriesPoint(execution_date=date(2024, 1, 1), avg_performance_score=70.0),
            TimeSeriesPoint(execution_date=date(2024, 1, 31), avg_performance_score=75.0),
        ]

        result = presenter.present(performance_metrics, mobile_ts, desktop_ts)

        # Check instance types
        assert isinstance(result, PerformanceViewModel)
        assert isinstance(result.mobile, DeviceMetricsViewModel)
        assert isinstance(result.desktop, DeviceMetricsViewModel)

        # Check mobile metrics
        assert result.mobile.device_label == "Mobile"
        assert result.mobile.target_card.value == "65.00"
        assert result.mobile.end_date_card.delta == "+10.00"
        assert result.mobile.growth_rate_display == "+20.00%"

        # Check desktop metrics
        assert result.desktop.device_label == "Desktop"
        assert result.desktop.target_card.value == "80.00"
        assert result.desktop.end_date_card.delta == "+5.00"

        # Check has time series data
        assert result.has_time_series_data is True

        # Check active filters
        assert len(result.active_filters_display) == 4

    def test_present_no_time_series(self, presenter, filter_criteria):
        """Test presentation with no time series data."""
        performance_metrics = PerformanceMetrics(
            mobile_metrics=DeviceMetrics(
                device="mobile", start_score=50.0, end_score=60.0
            ),
            desktop_metrics=DeviceMetrics(
                device="desktop", start_score=70.0, end_score=75.0
            ),
            filter_criteria=filter_criteria,
        )

        result = presenter.present(performance_metrics, [], [])

        assert result.has_time_series_data is False

    def test_present_only_mobile_time_series(self, presenter, filter_criteria):
        """Test presentation with only mobile time series."""
        performance_metrics = PerformanceMetrics(
            mobile_metrics=DeviceMetrics(
                device="mobile", start_score=50.0, end_score=60.0
            ),
            desktop_metrics=DeviceMetrics(
                device="desktop", start_score=70.0, end_score=75.0
            ),
            filter_criteria=filter_criteria,
        )

        mobile_ts = [
            TimeSeriesPoint(execution_date=date(2024, 1, 1), avg_performance_score=50.0),
        ]

        result = presenter.present(performance_metrics, mobile_ts, [])

        assert result.has_time_series_data is True

    def test_present_target_values(self, presenter, filter_criteria):
        """Test that target values are correctly applied."""
        performance_metrics = PerformanceMetrics(
            mobile_metrics=DeviceMetrics(
                device="mobile", start_score=50.0, end_score=60.0
            ),
            desktop_metrics=DeviceMetrics(
                device="desktop", start_score=70.0, end_score=75.0
            ),
            filter_criteria=filter_criteria,
        )

        result = presenter.present(performance_metrics, [], [])

        # Verify target constants
        assert presenter.TARGET_MOBILE == 65
        assert presenter.TARGET_DESKTOP == 80

        # Verify target values in view model
        assert result.mobile.target_card.value == "65.00"
        assert result.desktop.target_card.value == "80.00"


class TestPerformancePresenterEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def presenter(self):
        """Create presenter instance."""
        return PerformancePresenter()

    def test_very_small_positive_delta(self, presenter):
        """Test very small positive delta."""
        metrics = DeviceMetrics(device="mobile", start_score=50.0, end_score=50.01)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        assert result.end_date_card.delta == "+0.01"
        assert result.end_date_card.delta_color == "green"

    def test_very_small_negative_delta(self, presenter):
        """Test very small negative delta."""
        metrics = DeviceMetrics(device="mobile", start_score=50.0, end_score=49.99)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        assert result.end_date_card.delta == "-0.01"
        assert result.end_date_card.delta_color == "red"

    def test_large_positive_growth(self, presenter):
        """Test large positive growth rate."""
        metrics = DeviceMetrics(device="mobile", start_score=20.0, end_score=80.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        # (80 - 20) / 20 * 100 = 300%
        assert result.growth_rate_display == "+300.00%"
        assert result.growth_rate_color == "green"

    def test_large_negative_growth(self, presenter):
        """Test large negative growth rate."""
        metrics = DeviceMetrics(device="mobile", start_score=80.0, end_score=20.0)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        # (20 - 80) / 80 * 100 = -75%
        assert result.growth_rate_display == "-75.00%"
        assert result.growth_rate_color == "red"

    def test_floating_point_precision(self, presenter):
        """Test floating point precision in calculations."""
        metrics = DeviceMetrics(device="mobile", start_score=33.33, end_score=66.67)
        result = presenter._present_device_metrics(metrics, "Mobile", 65)

        # Delta should be precise
        assert result.end_date_card.delta == "+33.34"
        # Growth rate: (66.67 - 33.33) / 33.33 * 100 = 100.02%
        assert "+100" in result.growth_rate_display

"""
Tests for presentation view models.

Basic instantiation and immutability tests for all view models.
"""

from datetime import date

import pytest

from src.presentation.models.performance_view_model import (
    MetricCardViewModel,
    DeviceMetricsViewModel,
    PerformanceViewModel,
)
from src.presentation.models.competitor_view_model import (
    RankingViewModel,
    CompetitorViewModel,
)
from src.presentation.models.filter_view_model import (
    FilterOptionsViewModel,
    FilterSelectionViewModel,
)
from src.presentation.models.chart_view_model import (
    TimeSeriesDataPoint,
    TimeSeriesViewModel,
    ChartViewModel,
)


class TestMetricCardViewModel:
    """Test MetricCardViewModel instantiation."""

    def test_create_with_all_fields(self):
        """Test creating metric card with all fields."""
        card = MetricCardViewModel(
            label="Test Label",
            value="65.00",
            delta="+5.00",
            delta_color="green",
            help_text="Help text",
        )

        assert card.label == "Test Label"
        assert card.value == "65.00"
        assert card.delta == "+5.00"
        assert card.delta_color == "green"
        assert card.help_text == "Help text"

    def test_create_with_minimal_fields(self):
        """Test creating metric card with only required fields."""
        card = MetricCardViewModel(label="Label", value="50.00")

        assert card.label == "Label"
        assert card.value == "50.00"
        assert card.delta is None
        assert card.delta_color is None
        assert card.help_text is None

    def test_immutability(self):
        """Test that view model is immutable."""
        card = MetricCardViewModel(label="Label", value="50.00")

        with pytest.raises(Exception):  # dataclass frozen raises FrozenInstanceError
            card.value = "60.00"


class TestDeviceMetricsViewModel:
    """Test DeviceMetricsViewModel instantiation."""

    def test_create_complete(self):
        """Test creating device metrics with all fields."""
        target_card = MetricCardViewModel(label="Target", value="65.00")
        start_card = MetricCardViewModel(label="Start", value="50.00")
        end_card = MetricCardViewModel(label="End", value="60.00", delta="+10.00")

        device = DeviceMetricsViewModel(
            device_label="Mobile",
            target_card=target_card,
            start_date_card=start_card,
            end_date_card=end_card,
            growth_rate_display="+20.00%",
            growth_rate_color="green",
            has_data=True,
        )

        assert device.device_label == "Mobile"
        assert device.target_card == target_card
        assert device.growth_rate_display == "+20.00%"
        assert device.has_data is True

    def test_immutability(self):
        """Test that view model is immutable."""
        target_card = MetricCardViewModel(label="Target", value="65.00")
        start_card = MetricCardViewModel(label="Start", value="50.00")
        end_card = MetricCardViewModel(label="End", value="60.00")

        device = DeviceMetricsViewModel(
            device_label="Mobile",
            target_card=target_card,
            start_date_card=start_card,
            end_date_card=end_card,
            growth_rate_display="+20.00%",
            growth_rate_color="green",
            has_data=True,
        )

        with pytest.raises(Exception):
            device.device_label = "Desktop"


class TestPerformanceViewModel:
    """Test PerformanceViewModel instantiation."""

    def test_create_complete(self):
        """Test creating performance view model."""
        mobile = DeviceMetricsViewModel(
            device_label="Mobile",
            target_card=MetricCardViewModel(label="Target", value="65.00"),
            start_date_card=MetricCardViewModel(label="Start", value="50.00"),
            end_date_card=MetricCardViewModel(label="End", value="60.00"),
            growth_rate_display="+20.00%",
            growth_rate_color="green",
            has_data=True,
        )

        desktop = DeviceMetricsViewModel(
            device_label="Desktop",
            target_card=MetricCardViewModel(label="Target", value="80.00"),
            start_date_card=MetricCardViewModel(label="Start", value="70.00"),
            end_date_card=MetricCardViewModel(label="End", value="75.00"),
            growth_rate_display="+7.14%",
            growth_rate_color="green",
            has_data=True,
        )

        performance = PerformanceViewModel(
            mobile=mobile,
            desktop=desktop,
            active_filters_display=["Filter 1", "Filter 2"],
            has_time_series_data=True,
        )

        assert performance.mobile == mobile
        assert performance.desktop == desktop
        assert len(performance.active_filters_display) == 2
        assert performance.has_time_series_data is True


class TestRankingViewModel:
    """Test RankingViewModel instantiation."""

    def test_create_with_medal(self):
        """Test creating ranking with medal."""
        ranking = RankingViewModel(
            rank=1,
            brand="Brand A",
            score="85.50",
            medal="🥇",
            is_highlighted=True,
        )

        assert ranking.rank == 1
        assert ranking.brand == "Brand A"
        assert ranking.score == "85.50"
        assert ranking.medal == "🥇"
        assert ranking.is_highlighted is True

    def test_create_without_medal(self):
        """Test creating ranking without medal."""
        ranking = RankingViewModel(
            rank=5,
            brand="Brand E",
            score="70.00",
            medal="",
            is_highlighted=False,
        )

        assert ranking.rank == 5
        assert ranking.medal == ""
        assert ranking.is_highlighted is False

    def test_immutability(self):
        """Test that view model is immutable."""
        ranking = RankingViewModel(
            rank=1, brand="Brand A", score="85.50", medal="🥇", is_highlighted=True
        )

        with pytest.raises(Exception):
            ranking.rank = 2


class TestCompetitorViewModel:
    """Test CompetitorViewModel instantiation."""

    def test_create_complete(self):
        """Test creating competitor view model."""
        mobile_rankings = [
            RankingViewModel(
                rank=1, brand="Brand A", score="85.00", medal="🥇", is_highlighted=False
            ),
            RankingViewModel(
                rank=2, brand="Brand B", score="80.00", medal="🥈", is_highlighted=True
            ),
        ]

        desktop_rankings = [
            RankingViewModel(
                rank=1, brand="Brand X", score="90.00", medal="🥇", is_highlighted=True
            ),
        ]

        competitor = CompetitorViewModel(
            mobile_rankings=mobile_rankings,
            desktop_rankings=desktop_rankings,
            has_mobile_time_series=True,
            has_desktop_time_series=False,
            active_filters_display=["Filter 1"],
        )

        assert len(competitor.mobile_rankings) == 2
        assert len(competitor.desktop_rankings) == 1
        assert competitor.has_mobile_time_series is True
        assert competitor.has_desktop_time_series is False


class TestFilterOptionsViewModel:
    """Test FilterOptionsViewModel instantiation."""

    def test_create_complete(self):
        """Test creating filter options view model."""
        options = FilterOptionsViewModel(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brand_options=["All", "Brand A", "Brand B"],
            country_options=["All", "US", "UK"],
            page_type_options=["home", "product"],
            default_start_date=date(2024, 1, 1),
            default_end_date=date(2024, 12, 31),
        )

        assert options.min_date == date(2024, 1, 1)
        assert options.max_date == date(2024, 12, 31)
        assert len(options.brand_options) == 3
        assert options.brand_options[0] == "All"

    def test_immutability(self):
        """Test that view model is immutable."""
        options = FilterOptionsViewModel(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brand_options=["All", "Brand A"],
            country_options=["All", "US"],
            page_type_options=["home"],
            default_start_date=date(2024, 1, 1),
            default_end_date=date(2024, 12, 31),
        )

        with pytest.raises(Exception):
            options.min_date = date(2024, 2, 1)


class TestFilterSelectionViewModel:
    """Test FilterSelectionViewModel instantiation."""

    def test_create_complete(self):
        """Test creating filter selection view model."""
        selection = FilterSelectionViewModel(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            selected_brand="Brand A",
            selected_country="US",
            selected_page_types=["home", "product"],
            validation_error=None,
        )

        assert selection.start_date == date(2024, 1, 1)
        assert selection.end_date == date(2024, 1, 31)
        assert selection.selected_brand == "Brand A"
        assert selection.selected_country == "US"
        assert len(selection.selected_page_types) == 2

    def test_create_with_validation_error(self):
        """Test creating filter selection with validation error."""
        selection = FilterSelectionViewModel(
            start_date=date(2024, 1, 31),
            end_date=date(2024, 1, 1),
            selected_brand="All",
            selected_country="All",
            selected_page_types=[],
            validation_error="Start date must be before end date",
        )

        assert selection.validation_error == "Start date must be before end date"


class TestTimeSeriesDataPoint:
    """Test TimeSeriesDataPoint instantiation."""

    def test_create(self):
        """Test creating time series data point."""
        point = TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0)

        assert point.date == date(2024, 1, 1)
        assert point.value == 50.0

    def test_immutability(self):
        """Test that view model is immutable."""
        point = TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0)

        with pytest.raises(Exception):
            point.value = 60.0


class TestTimeSeriesViewModel:
    """Test TimeSeriesViewModel instantiation."""

    def test_create_complete(self):
        """Test creating time series view model."""
        data_points = [
            TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0),
            TimeSeriesDataPoint(date=date(2024, 1, 15), value=60.0),
            TimeSeriesDataPoint(date=date(2024, 1, 31), value=70.0),
        ]

        series = TimeSeriesViewModel(
            series_name="Mobile",
            data_points=data_points,
            color="blue",
            line_width=2,
            marker_size=6,
        )

        assert series.series_name == "Mobile"
        assert len(series.data_points) == 3
        assert series.color == "blue"
        assert series.line_width == 2
        assert series.marker_size == 6

    def test_create_with_defaults(self):
        """Test creating time series with default values."""
        data_points = [TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0)]

        series = TimeSeriesViewModel(
            series_name="Mobile", data_points=data_points, color="blue"
        )

        assert series.line_width == 2  # Default value
        assert series.marker_size == 4  # Default value


class TestChartViewModel:
    """Test ChartViewModel instantiation."""

    def test_create_complete(self):
        """Test creating chart view model."""
        series = [
            TimeSeriesViewModel(
                series_name="Mobile",
                data_points=[TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0)],
                color="blue",
            ),
        ]

        chart = ChartViewModel(
            title="Performance Evolution",
            series=series,
            y_axis_label="Score",
            show_thresholds=True,
            red_threshold=40.0,
            green_threshold=60.0,
            height=600,
        )

        assert chart.title == "Performance Evolution"
        assert len(chart.series) == 1
        assert chart.y_axis_label == "Score"
        assert chart.show_thresholds is True
        assert chart.red_threshold == 40.0
        assert chart.green_threshold == 60.0
        assert chart.height == 600

    def test_create_with_defaults(self):
        """Test creating chart with default values."""
        chart = ChartViewModel(
            title="Test Chart", series=[], y_axis_label="Score", show_thresholds=False
        )

        assert chart.red_threshold is None  # Default
        assert chart.green_threshold is None  # Default
        assert chart.height == 500  # Default

    def test_create_without_thresholds(self):
        """Test creating chart without thresholds."""
        chart = ChartViewModel(
            title="Test Chart",
            series=[],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        assert chart.show_thresholds is False
        assert chart.red_threshold is None
        assert chart.green_threshold is None

    def test_immutability(self):
        """Test that view model is immutable."""
        chart = ChartViewModel(
            title="Test Chart", series=[], y_axis_label="Score", show_thresholds=False
        )

        with pytest.raises(Exception):
            chart.title = "New Title"


class TestViewModelIntegration:
    """Integration tests for view models working together."""

    def test_complete_performance_view_model_structure(self):
        """Test creating complete performance view model structure."""
        # Create cards
        mobile_target = MetricCardViewModel(label="Target", value="65.00")
        mobile_start = MetricCardViewModel(label="Start", value="50.00")
        mobile_end = MetricCardViewModel(
            label="End", value="60.00", delta="+10.00", delta_color="green"
        )

        # Create device metrics
        mobile = DeviceMetricsViewModel(
            device_label="Mobile",
            target_card=mobile_target,
            start_date_card=mobile_start,
            end_date_card=mobile_end,
            growth_rate_display="+20.00%",
            growth_rate_color="green",
            has_data=True,
        )

        desktop = DeviceMetricsViewModel(
            device_label="Desktop",
            target_card=MetricCardViewModel(label="Target", value="80.00"),
            start_date_card=MetricCardViewModel(label="Start", value="70.00"),
            end_date_card=MetricCardViewModel(label="End", value="75.00"),
            growth_rate_display="+7.14%",
            growth_rate_color="green",
            has_data=True,
        )

        # Create performance view model
        performance = PerformanceViewModel(
            mobile=mobile,
            desktop=desktop,
            active_filters_display=["From 2024-01-01 to 2024-01-31"],
            has_time_series_data=True,
        )

        # Verify structure
        assert performance.mobile.device_label == "Mobile"
        assert performance.mobile.end_date_card.delta == "+10.00"
        assert performance.desktop.device_label == "Desktop"

    def test_complete_competitor_view_model_structure(self):
        """Test creating complete competitor view model structure."""
        # Create rankings
        mobile_rankings = [
            RankingViewModel(
                rank=1,
                brand="Brand A",
                score="85.50",
                medal="🥇",
                is_highlighted=False,
            ),
            RankingViewModel(
                rank=2,
                brand="Our Brand",
                score="80.25",
                medal="🥈",
                is_highlighted=True,
            ),
            RankingViewModel(
                rank=3,
                brand="Brand C",
                score="75.00",
                medal="🥉",
                is_highlighted=False,
            ),
        ]

        # Create competitor view model
        competitor = CompetitorViewModel(
            mobile_rankings=mobile_rankings,
            desktop_rankings=[],
            has_mobile_time_series=True,
            has_desktop_time_series=False,
            active_filters_display=["From 2024-01-01 to 2024-01-31"],
        )

        # Verify structure
        assert len(competitor.mobile_rankings) == 3
        assert competitor.mobile_rankings[1].is_highlighted is True
        assert competitor.mobile_rankings[0].medal == "🥇"

    def test_complete_chart_view_model_structure(self):
        """Test creating complete chart view model structure."""
        # Create data points
        mobile_points = [
            TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0),
            TimeSeriesDataPoint(date=date(2024, 1, 15), value=55.0),
            TimeSeriesDataPoint(date=date(2024, 1, 31), value=60.0),
        ]

        desktop_points = [
            TimeSeriesDataPoint(date=date(2024, 1, 1), value=70.0),
            TimeSeriesDataPoint(date=date(2024, 1, 15), value=72.0),
            TimeSeriesDataPoint(date=date(2024, 1, 31), value=75.0),
        ]

        # Create series
        series = [
            TimeSeriesViewModel(
                series_name="Mobile",
                data_points=mobile_points,
                color="blue",
                line_width=2,
                marker_size=6,
            ),
            TimeSeriesViewModel(
                series_name="Desktop",
                data_points=desktop_points,
                color="green",
                line_width=2,
                marker_size=6,
            ),
        ]

        # Create chart
        chart = ChartViewModel(
            title="Performance Evolution",
            series=series,
            y_axis_label="Performance Score",
            show_thresholds=True,
            red_threshold=40.0,
            green_threshold=60.0,
            height=500,
        )

        # Verify structure
        assert len(chart.series) == 2
        assert chart.series[0].series_name == "Mobile"
        assert len(chart.series[0].data_points) == 3
        assert chart.series[1].series_name == "Desktop"

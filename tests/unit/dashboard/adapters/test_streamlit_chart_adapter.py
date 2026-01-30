"""
Tests for StreamlitChartAdapter.

Tests chart view model to Plotly figure conversion:
- Series rendering
- Layout configuration
- Threshold lines
- Chart styling
"""

from datetime import date
from unittest.mock import Mock, patch, MagicMock

import pytest

from src.presentation.models.chart_view_model import (
    ChartViewModel,
    TimeSeriesViewModel,
    TimeSeriesDataPoint,
)
from src.dashboard.adapters.streamlit_chart_adapter import StreamlitChartAdapter


class TestStreamlitChartAdapter:
    """Test suite for StreamlitChartAdapter."""

    @pytest.fixture
    def adapter(self):
        """Create adapter instance with default thresholds."""
        return StreamlitChartAdapter(red_threshold=40.0, green_threshold=60.0)

    @pytest.fixture
    def simple_chart_vm(self):
        """Create simple chart view model."""
        return ChartViewModel(
            title="Test Chart",
            series=[
                TimeSeriesViewModel(
                    series_name="Series 1",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0),
                        TimeSeriesDataPoint(date=date(2024, 1, 15), value=60.0),
                        TimeSeriesDataPoint(date=date(2024, 1, 31), value=70.0),
                    ],
                    color="blue",
                    line_width=2,
                    marker_size=6,
                )
            ],
            y_axis_label="Score",
            show_thresholds=False,
            red_threshold=None,
            green_threshold=None,
            height=500,
        )

    # Test initialization
    def test_adapter_initialization_with_defaults(self):
        """Test adapter initializes with default threshold values."""
        adapter = StreamlitChartAdapter()

        assert adapter.chart_renderer is not None
        # Default values from signature
        assert hasattr(adapter, "chart_renderer")

    def test_adapter_initialization_with_custom_thresholds(self):
        """Test adapter initializes with custom threshold values."""
        adapter = StreamlitChartAdapter(red_threshold=30.0, green_threshold=70.0)

        assert adapter.chart_renderer is not None
        assert adapter.chart_renderer.red_threshold == 30.0
        assert adapter.chart_renderer.green_threshold == 70.0

    # Test render_chart - Basic functionality
    def test_render_chart_returns_figure(self, adapter, simple_chart_vm):
        """Test that render_chart returns a Plotly Figure object."""
        import plotly.graph_objects as go

        result = adapter.render_chart(simple_chart_vm)

        assert isinstance(result, go.Figure)

    def test_render_chart_with_single_series(self, adapter, simple_chart_vm):
        """Test rendering chart with single series."""
        result = adapter.render_chart(simple_chart_vm)

        # Should have one trace
        assert len(result.data) == 1

        # Check trace properties
        trace = result.data[0]
        assert trace.name == "Series 1"
        assert len(trace.x) == 3
        assert len(trace.y) == 3
        assert list(trace.y) == [50.0, 60.0, 70.0]

    def test_render_chart_with_multiple_series(self, adapter):
        """Test rendering chart with multiple series."""
        chart_vm = ChartViewModel(
            title="Multi-Series Chart",
            series=[
                TimeSeriesViewModel(
                    series_name="Mobile",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0),
                        TimeSeriesDataPoint(date=date(2024, 1, 31), value=60.0),
                    ],
                    color="blue",
                    line_width=2,
                    marker_size=6,
                ),
                TimeSeriesViewModel(
                    series_name="Desktop",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=70.0),
                        TimeSeriesDataPoint(date=date(2024, 1, 31), value=80.0),
                    ],
                    color="green",
                    line_width=2,
                    marker_size=6,
                ),
            ],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        result = adapter.render_chart(chart_vm)

        # Should have two traces
        assert len(result.data) == 2
        assert result.data[0].name == "Mobile"
        assert result.data[1].name == "Desktop"

    def test_render_chart_empty_series(self, adapter):
        """Test rendering chart with no series."""
        chart_vm = ChartViewModel(
            title="Empty Chart",
            series=[],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        result = adapter.render_chart(chart_vm)

        # Should have no traces
        assert len(result.data) == 0

    # Test chart configuration
    def test_render_chart_title(self, adapter, simple_chart_vm):
        """Test that chart title is set correctly."""
        result = adapter.render_chart(simple_chart_vm)

        assert result.layout.title.text == "Test Chart"

    def test_render_chart_y_axis_label(self, adapter, simple_chart_vm):
        """Test that y-axis label is set correctly."""
        result = adapter.render_chart(simple_chart_vm)

        assert result.layout.yaxis.title.text == "Score"

    def test_render_chart_height(self, adapter):
        """Test that chart height is set correctly."""
        chart_vm = ChartViewModel(
            title="Test Chart",
            series=[],
            y_axis_label="Score",
            show_thresholds=False,
            height=600,
        )

        result = adapter.render_chart(chart_vm)

        assert result.layout.height == 600

    def test_render_chart_custom_height(self, adapter):
        """Test chart with custom height."""
        chart_vm = ChartViewModel(
            title="Test Chart",
            series=[],
            y_axis_label="Score",
            show_thresholds=False,
            height=800,
        )

        result = adapter.render_chart(chart_vm)

        assert result.layout.height == 800

    # Test series styling
    def test_render_chart_series_color(self, adapter, simple_chart_vm):
        """Test that series color is applied correctly."""
        result = adapter.render_chart(simple_chart_vm)

        trace = result.data[0]
        assert trace.line.color == "blue"

    def test_render_chart_series_line_width(self, adapter, simple_chart_vm):
        """Test that series line width is applied correctly."""
        result = adapter.render_chart(simple_chart_vm)

        trace = result.data[0]
        assert trace.line.width == 2

    def test_render_chart_series_marker_size(self, adapter, simple_chart_vm):
        """Test that series marker size is applied correctly."""
        result = adapter.render_chart(simple_chart_vm)

        trace = result.data[0]
        assert trace.marker.size == 6

    def test_render_chart_series_without_color(self, adapter):
        """Test series with None color defaults to blue."""
        chart_vm = ChartViewModel(
            title="Test Chart",
            series=[
                TimeSeriesViewModel(
                    series_name="Series",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0),
                    ],
                    color=None,
                    line_width=2,
                    marker_size=6,
                )
            ],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        result = adapter.render_chart(chart_vm)

        trace = result.data[0]
        assert trace.line.color == "blue"  # Default color

    # Test thresholds
    def test_render_chart_with_thresholds_calls_renderer(self, adapter):
        """Test that thresholds are added when show_thresholds is True."""
        chart_vm = ChartViewModel(
            title="Test Chart",
            series=[
                TimeSeriesViewModel(
                    series_name="Series",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0),
                    ],
                    color="blue",
                    line_width=2,
                    marker_size=6,
                )
            ],
            y_axis_label="Score",
            show_thresholds=True,
            red_threshold=40.0,
            green_threshold=60.0,
            height=500,
        )

        with patch.object(
            adapter.chart_renderer, "_add_threshold_lines"
        ) as mock_threshold:
            result = adapter.render_chart(chart_vm)
            mock_threshold.assert_called_once()

    def test_render_chart_without_thresholds_skips_renderer(self, adapter):
        """Test that thresholds are not added when show_thresholds is False."""
        chart_vm = ChartViewModel(
            title="Test Chart",
            series=[
                TimeSeriesViewModel(
                    series_name="Series",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0),
                    ],
                    color="blue",
                    line_width=2,
                    marker_size=6,
                )
            ],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        with patch.object(
            adapter.chart_renderer, "_add_threshold_lines"
        ) as mock_threshold:
            result = adapter.render_chart(chart_vm)
            mock_threshold.assert_not_called()

    # Test data points
    def test_render_chart_date_values(self, adapter, simple_chart_vm):
        """Test that date values are correctly extracted."""
        result = adapter.render_chart(simple_chart_vm)

        trace = result.data[0]
        expected_dates = [date(2024, 1, 1), date(2024, 1, 15), date(2024, 1, 31)]
        assert list(trace.x) == expected_dates

    def test_render_chart_numeric_values(self, adapter, simple_chart_vm):
        """Test that numeric values are correctly extracted."""
        result = adapter.render_chart(simple_chart_vm)

        trace = result.data[0]
        assert list(trace.y) == [50.0, 60.0, 70.0]

    def test_render_chart_single_data_point(self, adapter):
        """Test rendering with single data point."""
        chart_vm = ChartViewModel(
            title="Single Point",
            series=[
                TimeSeriesViewModel(
                    series_name="Series",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=75.0),
                    ],
                    color="blue",
                    line_width=2,
                    marker_size=6,
                )
            ],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        result = adapter.render_chart(chart_vm)

        trace = result.data[0]
        assert len(trace.x) == 1
        assert len(trace.y) == 1
        assert trace.y[0] == 75.0

    # Test layout configuration
    def test_render_chart_grid_configuration(self, adapter, simple_chart_vm):
        """Test that grid is enabled for both axes."""
        result = adapter.render_chart(simple_chart_vm)

        assert result.layout.xaxis.showgrid is True
        assert result.layout.yaxis.showgrid is True

    def test_render_chart_hover_mode(self, adapter, simple_chart_vm):
        """Test that hover mode is set to x unified."""
        result = adapter.render_chart(simple_chart_vm)

        assert result.layout.hovermode == "x unified"

    def test_render_chart_legend_configuration(self, adapter, simple_chart_vm):
        """Test legend configuration."""
        result = adapter.render_chart(simple_chart_vm)

        legend = result.layout.legend
        assert legend.orientation == "h"
        assert legend.yanchor == "bottom"
        assert legend.y == 1.02
        assert legend.xanchor == "right"
        assert legend.x == 1


class TestStreamlitChartAdapterEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def adapter(self):
        """Create adapter instance."""
        return StreamlitChartAdapter(red_threshold=40.0, green_threshold=60.0)

    def test_render_chart_with_many_series(self, adapter):
        """Test rendering chart with many series."""
        # Use valid Plotly colors
        colors = ["blue", "red", "green", "orange", "purple", "brown", "pink", "gray", "olive", "cyan"]
        series_list = []
        for i in range(10):
            series_list.append(
                TimeSeriesViewModel(
                    series_name=f"Series {i}",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=float(i * 10)),
                    ],
                    color=colors[i],
                    line_width=2,
                    marker_size=6,
                )
            )

        chart_vm = ChartViewModel(
            title="Many Series",
            series=series_list,
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        result = adapter.render_chart(chart_vm)

        assert len(result.data) == 10

    def test_render_chart_with_many_data_points(self, adapter):
        """Test rendering with many data points."""
        data_points = [
            TimeSeriesDataPoint(date=date(2024, 1, i), value=float(i))
            for i in range(1, 32)  # 31 data points
        ]

        chart_vm = ChartViewModel(
            title="Many Points",
            series=[
                TimeSeriesViewModel(
                    series_name="Series",
                    data_points=data_points,
                    color="blue",
                    line_width=2,
                    marker_size=6,
                )
            ],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        result = adapter.render_chart(chart_vm)

        trace = result.data[0]
        assert len(trace.x) == 31
        assert len(trace.y) == 31

    def test_render_chart_with_zero_values(self, adapter):
        """Test rendering with zero values."""
        chart_vm = ChartViewModel(
            title="Zero Values",
            series=[
                TimeSeriesViewModel(
                    series_name="Series",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=0.0),
                        TimeSeriesDataPoint(date=date(2024, 1, 2), value=0.0),
                    ],
                    color="blue",
                    line_width=2,
                    marker_size=6,
                )
            ],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        result = adapter.render_chart(chart_vm)

        trace = result.data[0]
        assert list(trace.y) == [0.0, 0.0]

    def test_render_chart_with_negative_values(self, adapter):
        """Test rendering with negative values."""
        chart_vm = ChartViewModel(
            title="Negative Values",
            series=[
                TimeSeriesViewModel(
                    series_name="Series",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=-10.0),
                        TimeSeriesDataPoint(date=date(2024, 1, 2), value=-5.0),
                    ],
                    color="blue",
                    line_width=2,
                    marker_size=6,
                )
            ],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        result = adapter.render_chart(chart_vm)

        trace = result.data[0]
        assert list(trace.y) == [-10.0, -5.0]

    def test_render_chart_with_very_large_values(self, adapter):
        """Test rendering with very large values."""
        chart_vm = ChartViewModel(
            title="Large Values",
            series=[
                TimeSeriesViewModel(
                    series_name="Series",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=1000000.0),
                        TimeSeriesDataPoint(date=date(2024, 1, 2), value=2000000.0),
                    ],
                    color="blue",
                    line_width=2,
                    marker_size=6,
                )
            ],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        result = adapter.render_chart(chart_vm)

        trace = result.data[0]
        assert trace.y[0] == 1000000.0
        assert trace.y[1] == 2000000.0

    def test_render_chart_with_special_characters_in_title(self, adapter):
        """Test chart with special characters in title."""
        chart_vm = ChartViewModel(
            title="Test & Chart <with> 'special' \"characters\"",
            series=[],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        result = adapter.render_chart(chart_vm)

        assert "Test & Chart" in result.layout.title.text

    def test_adapter_with_zero_thresholds(self):
        """Test adapter with zero threshold values."""
        adapter = StreamlitChartAdapter(red_threshold=0.0, green_threshold=0.0)

        assert adapter.chart_renderer.red_threshold == 0.0
        assert adapter.chart_renderer.green_threshold == 0.0

    def test_render_chart_preserves_date_order(self, adapter):
        """Test that data points maintain their order."""
        chart_vm = ChartViewModel(
            title="Ordered Data",
            series=[
                TimeSeriesViewModel(
                    series_name="Series",
                    data_points=[
                        TimeSeriesDataPoint(date=date(2024, 1, 31), value=70.0),
                        TimeSeriesDataPoint(date=date(2024, 1, 1), value=50.0),
                        TimeSeriesDataPoint(date=date(2024, 1, 15), value=60.0),
                    ],
                    color="blue",
                    line_width=2,
                    marker_size=6,
                )
            ],
            y_axis_label="Score",
            show_thresholds=False,
            height=500,
        )

        result = adapter.render_chart(chart_vm)

        trace = result.data[0]
        # Should maintain input order
        expected_dates = [date(2024, 1, 31), date(2024, 1, 1), date(2024, 1, 15)]
        assert list(trace.x) == expected_dates

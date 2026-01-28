"""
Framework-agnostic chart builder.

Transforms DTOs into chart view models that can be rendered by any
charting library (Plotly, Chart.js, D3, etc.).
"""

from typing import List, Dict, Optional

from src.application.dto.dashboard_dtos import TimeSeriesPoint
from src.presentation.models.chart_view_model import (
    ChartViewModel,
    TimeSeriesViewModel,
    TimeSeriesDataPoint,
)


class ChartBuilder:
    """
    Builds chart view models from business data.

    Provides framework-agnostic chart configurations that can be
    adapted to any charting library.
    """

    def __init__(
        self, red_threshold: float = 40.0, green_threshold: float = 60.0
    ):
        """
        Initialize chart builder with threshold values.

        Args:
            red_threshold: Lower threshold for performance (default 40.0)
            green_threshold: Upper threshold for performance (default 60.0)
        """
        self.red_threshold = red_threshold
        self.green_threshold = green_threshold

    def build_performance_evolution_chart(
        self,
        mobile_data: List[TimeSeriesPoint],
        desktop_data: List[TimeSeriesPoint],
    ) -> ChartViewModel:
        """
        Build performance evolution chart model.

        Args:
            mobile_data: Mobile time series data
            desktop_data: Desktop time series data

        Returns:
            Chart view model with mobile and desktop series
        """
        series = []

        if mobile_data:
            mobile_series = TimeSeriesViewModel(
                series_name="Mobile",
                data_points=[
                    TimeSeriesDataPoint(
                        date=point.execution_date,
                        value=point.avg_performance_score or 0.0,
                    )
                    for point in mobile_data
                ],
                color="red",
                line_width=3,
                marker_size=8,
            )
            series.append(mobile_series)

        if desktop_data:
            desktop_series = TimeSeriesViewModel(
                series_name="Desktop",
                data_points=[
                    TimeSeriesDataPoint(
                        date=point.execution_date,
                        value=point.avg_performance_score or 0.0,
                    )
                    for point in desktop_data
                ],
                color="royalblue",
                line_width=3,
                marker_size=8,
            )
            series.append(desktop_series)

        return ChartViewModel(
            title="Performance Score Evolution",
            series=series,
            y_axis_label="Performance Score",
            show_thresholds=True,
            red_threshold=self.red_threshold,
            green_threshold=self.green_threshold,
            height=500,
        )

    def build_competitor_evolution_chart(
        self,
        time_series_data: List[TimeSeriesPoint],
        device: str,
        target_brands: List[str],
        target_brand_colors: Optional[Dict[str, str]] = None,
    ) -> ChartViewModel:
        """
        Build competitor evolution chart model.

        Args:
            time_series_data: Time series data for all brands
            device: Device type ("mobile" or "desktop")
            target_brands: List of target brand names to highlight
            target_brand_colors: Optional color mapping for target brands

        Returns:
            Chart view model with per-brand series
        """
        # Group by brand
        brands: Dict[str, List[TimeSeriesPoint]] = {}
        for point in time_series_data:
            if point.brand:
                if point.brand not in brands:
                    brands[point.brand] = []
                brands[point.brand].append(point)

        # Build color palette
        if target_brand_colors is None:
            target_colors = ["red", "royalblue", "purple", "cyan"]
            target_brand_colors = {
                brand: target_colors[i % len(target_colors)]
                for i, brand in enumerate(target_brands)
            }

        default_colors = ["green", "orange", "skyblue", "pink", "silver"]
        color_idx = 0

        # Build series for each brand
        series = []
        for brand, points in brands.items():
            if brand in target_brands:
                color = target_brand_colors.get(brand, "#a7f9ab")
                line_width = 3
                marker_size = 6
            else:
                color = default_colors[color_idx % len(default_colors)]
                color_idx += 1
                line_width = 2
                marker_size = 4

            series.append(
                TimeSeriesViewModel(
                    series_name=brand,
                    data_points=[
                        TimeSeriesDataPoint(
                            date=p.execution_date,
                            value=p.avg_performance_score or 0.0,
                            label=brand,
                        )
                        for p in points
                    ],
                    color=color,
                    line_width=line_width,
                    marker_size=marker_size,
                )
            )

        return ChartViewModel(
            title=f"{device.capitalize()} Evolution",
            series=series,
            y_axis_label="Performance Score",
            show_thresholds=True,
            red_threshold=self.red_threshold,
            green_threshold=self.green_threshold,
            height=500,
        )

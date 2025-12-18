"""
Dashboard chart utilities using Plotly.

This module provides functions for creating interactive charts
for the dashboard.
"""

from typing import List

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.application.dto.dashboard_dtos import TimeSeriesPoint
from src.dashboard.components.chart_renderer import ChartRenderer


def create_performance_evolution_chart(
    mobile_data: List[TimeSeriesPoint],
    desktop_data: List[TimeSeriesPoint],
) -> go.Figure:
    """
    Create a line chart showing performance evolution for mobile and desktop.

    Args:
        mobile_data: List of time series points for mobile
        desktop_data: List of time series points for desktop

    Returns:
        Plotly Figure object
    """
    renderer = ChartRenderer()
    
    return renderer.create_performance_evolution_chart(mobile_data=mobile_data, desktop_data=desktop_data)


def create_competitor_evolution_chart(
    time_series_data: List[TimeSeriesPoint],
    device: str,
    target_brands: List[str],
    target_brand_colors: dict = None,
) -> go.Figure:
    """
    Create a line chart showing performance evolution for multiple brands.

    Args:
        time_series_data: List of time series points with brand information
        device: Device type for the chart title
        target_brands: List of brands to highlight (thicker lines, custom colors)
        target_brand_colors: Optional dict mapping target brands to hex colors

    Returns:
        Plotly Figure object
    """
    renderer = ChartRenderer()
    return renderer.create_competitor_evolution_chart(
        time_series_data=time_series_data,
        device=device,
        target_brands=target_brands,
        target_brand_colors=target_brand_colors,
    )

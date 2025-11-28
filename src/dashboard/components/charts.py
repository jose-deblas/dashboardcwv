"""
Dashboard chart utilities using Plotly.

This module provides functions for creating interactive charts
for the dashboard.
"""

from typing import List

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.application.dto.dashboard_dtos import TimeSeriesPoint


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
    fig = go.Figure()

    all_dates = []
    if mobile_data:
        all_dates.extend([point.execution_date for point in mobile_data])
    if desktop_data:
        all_dates.extend([point.execution_date for point in desktop_data]) 
    if all_dates:
        min_date = min(all_dates)
        max_date = max(all_dates)

    # Mobile trace
    if mobile_data:
        mobile_dates = [point.execution_date for point in mobile_data]
        mobile_scores = [point.avg_performance_score for point in mobile_data]

        fig.add_trace(
            go.Scatter(
                x=mobile_dates,
                y=mobile_scores,
                mode="lines+markers",
                name="Mobile",
                line=dict(color="red", width=3), #line=dict(color="#a7f9ab", width=3),
                marker=dict(size=8),
                hovertemplate="Mobile: %{y:.2f}<extra></extra>",
            )
        )

    # Desktop trace
    if desktop_data:
        desktop_dates = [point.execution_date for point in desktop_data]
        desktop_scores = [point.avg_performance_score for point in desktop_data]

        fig.add_trace(
            go.Scatter(
                x=desktop_dates,
                y=desktop_scores,
                mode="lines+markers",
                name="Desktop",
                line=dict(color="royalblue", width=3),#line=dict(color="#4a9eff", width=3),
                marker=dict(size=8),
                hovertemplate="Desktop: %{y:.2f}<extra></extra>",
            )
        )

    # Layout
    fig.update_layout(
        xaxis=dict(
            showgrid=True,
        ),
        yaxis=dict(
            title="Performance Score",
            showgrid=True,
            range=[min_date, max_date],
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12),
        ),
        height=500,
    )

    return fig


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
    fig = go.Figure()

    # Group data by brand
    brands = {}
    for point in time_series_data:
        if point.brand not in brands:
            brands[point.brand] = {"dates": [], "scores": []}
        brands[point.brand]["dates"].append(point.execution_date)
        brands[point.brand]["scores"].append(point.avg_performance_score)

    #take the min and max score to set y axis range
    all_scores = []
    for data in brands.values():
        all_scores.extend(data["scores"])
    if all_scores:
        min_score = min(all_scores) - 1
        max_score = max(all_scores) + 1

    # Build color palette for target brands
    if target_brand_colors is None:
        # Default colors for target brands if not provided
        target_colors = ["red", "royalblue", "purple", "cyan"]
        target_brand_colors = {
            brand: target_colors[i % len(target_colors)]
            for i, brand in enumerate(target_brands)
        }

    # Default colors for non-target brands
    default_colors = ["green", "yellow", "orange", "pink", "silver"]
    color_idx = 0

    # Add trace for each brand
    for brand, data in brands.items():
        if brand in target_brands:
            color = target_brand_colors.get(brand, "#a7f9ab")
            line_width = 3
            marker_size = 6
        else:
            color = default_colors[color_idx % len(default_colors)]
            color_idx += 1
            line_width = 2
            marker_size = 4

        fig.add_trace(
            go.Scatter(
                x=data["dates"],
                y=data["scores"],
                mode="lines+markers",
                name=brand,
                line=dict(color=color, width=line_width),
                marker=dict(size=marker_size),
                hovertemplate=f"<b>{brand}</b>: %{{y:.2f}}<extra></extra>",
            )
        )

    # Layout
    fig.update_layout(
        title=dict(
            text=f" {device.capitalize()}",
            #font=dict(size=20, color="#a7f9ab"),
        ),
        xaxis=dict(
            #title="Date",
            showgrid=True,
            #gridcolor="#333",
            #color="#fff",
        ),
        yaxis=dict(
            title="Performance Score",
            showgrid=True,
            #gridcolor="#333",
            range=[min_score, max_score],
            #color="#fff",
        ),
        #plot_bgcolor="#1e1e1e",
        #paper_bgcolor="#262730",
        #font=dict(color="#fff"),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12),
        ),
        height=500,
    )

    return fig

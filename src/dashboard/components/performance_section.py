"""
Performance section component.

This module provides the performance section of the dashboard,
including metrics cards and evolution charts.
"""

from typing import List

import streamlit as st

from src.application.dto.dashboard_dtos import DeviceMetrics, TimeSeriesPoint
from src.dashboard.components.charts import create_performance_evolution_chart
from src.dashboard.components.styles import get_weather_give_traffic_light_color


def render_device_metrics(device_metrics: DeviceMetrics):
    """
    Render performance metrics for a single device.

    Args:
        device_metrics: Device metrics to display
    """
    device_label = device_metrics.device.capitalize()

    # Check if we have data
    if device_metrics.start_score is None and device_metrics.end_score is None:
        st.warning(f"No data available for {device_label}")
        return

    st.markdown(
        """
        <style>
        div[data-testid="stMetricDelta"] {
            font-size: 1.5em;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    # Start score
    with col1:
        start_score_value = f"{device_metrics.start_score:.2f}" if device_metrics.start_score is not None else "N/A"
        st.metric(
            "**Initial Date**",
            value=start_score_value,
            delta=None,
            width="content",
        )

    # End score
    with col2:
        end_score_value = f"{device_metrics.end_score:.2f}" if device_metrics.end_score is not None else "N/A"
        delta_value = f"{device_metrics.delta:.2f}" if device_metrics.delta is not None else None
        st.metric(
            "**End Date**",
            value=end_score_value,
            delta=delta_value,
            width="content",
        )

    with col3:
        weather_character = get_weather_give_traffic_light_color(device_metrics.traffic_light)
        st.markdown(f"<h2>{weather_character}</h2>", unsafe_allow_html=True)

def render_performance_section(
    mobile_metrics: DeviceMetrics,
    desktop_metrics: DeviceMetrics,
    mobile_time_series: List[TimeSeriesPoint],
    desktop_time_series: List[TimeSeriesPoint],
):
    """
    Render the complete performance section.

    Args:
        mobile_metrics: Mobile device metrics
        desktop_metrics: Desktop device metrics
        mobile_time_series: Mobile time series data
        desktop_time_series: Desktop time series data
    """
    st.markdown(
        '<h2 class="highlight">📊 Performance Score</h2>',
        unsafe_allow_html=True,
        help="The Core Web Vitals performance score is based on real-world user data (field data) and is determined by three metrics: Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS)"
    )

    col1, col2 = st.columns(2)

    with col1.container(border=True, height="stretch"):
        st.markdown("### 📱 Mobile")
        render_device_metrics(mobile_metrics)

    with col2.container(border=True, height="stretch"):
        st.markdown("### 💻 Desktop")
        render_device_metrics(desktop_metrics)

    
    # Evolution chart
    st.markdown("### Performance Score Evolution")

    if not mobile_time_series and not desktop_time_series:
        st.warning("No time series data available for the selected filters")
    else:
        fig = create_performance_evolution_chart(
            mobile_data=mobile_time_series,
            desktop_data=desktop_time_series,
        )
        st.plotly_chart(fig, use_container_width=True)

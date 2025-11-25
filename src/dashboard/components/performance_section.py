"""
Performance section component.

This module provides the performance section of the dashboard,
including metrics cards and evolution charts.
"""

from typing import List

import streamlit as st

from src.application.dto.dashboard_dtos import DeviceMetrics, TimeSeriesPoint
from src.dashboard.components.charts import create_performance_evolution_chart
from src.dashboard.components.styles import get_traffic_light_html


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

    col1, col2, col3 = st.columns(3)

    # Start score
    with col1:
        st.markdown(f"**{device_label} - Start Date**")
        if device_metrics.start_score is not None:
            st.markdown(
                get_traffic_light_html("amber", device_metrics.start_score),
                unsafe_allow_html=True,
            )
        else:
            st.info("No data")

    # End score
    with col2:
        st.markdown(f"**{device_label} - End Date**")
        if device_metrics.end_score is not None:
            traffic_light_color = device_metrics.traffic_light
            st.markdown(
                get_traffic_light_html(
                    traffic_light_color,
                    device_metrics.end_score,
                    device_metrics.delta,
                ),
                unsafe_allow_html=True,
            )
        else:
            st.info("No data")

    # Delta
    with col3:
        st.markdown(f"**{device_label} - Change**")
        if device_metrics.delta is not None:
            delta_value = device_metrics.delta
            if delta_value > 0:
                st.success(f"⬆️ +{delta_value:.2f} points")
            elif delta_value < 0:
                st.error(f"⬇️ {delta_value:.2f} points")
            else:
                st.warning("➡️ No change")
        else:
            st.info("N/A")


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
    st.markdown('<h2 class="highlight">📊 Performance Overview</h2>', unsafe_allow_html=True)

    # Display metrics for both devices
    st.markdown("### Mobile Performance")
    render_device_metrics(mobile_metrics)

    st.markdown("---")

    st.markdown("### Desktop Performance")
    render_device_metrics(desktop_metrics)

    st.markdown("---")

    # Evolution chart
    st.markdown("### Performance Evolution")

    if not mobile_time_series and not desktop_time_series:
        st.warning("No time series data available for the selected filters")
    else:
        fig = create_performance_evolution_chart(
            mobile_data=mobile_time_series,
            desktop_data=desktop_time_series,
            title="Performance Score Evolution Over Time",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

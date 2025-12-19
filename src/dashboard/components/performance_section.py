"""
Performance section component.

This module provides the performance section of the dashboard,
including metrics cards and evolution charts.
"""

from typing import List

import streamlit as st

from src.application.dto.dashboard_dtos import DeviceMetrics, TimeSeriesPoint, FilterCriteria
from src.dashboard.components.charts import create_performance_evolution_chart
from src.dashboard.components.styles import get_growth_color
from src.dashboard.components.filters import display_active_filters


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

    col1, col2, col3, col4 = st.columns(4)

    # Start score
    with col1:
        start_score_value = f"{device_metrics.start_score:.2f}" if device_metrics.start_score is not None else "N/A"
        st.metric(
            "**Target**",
            value=device_metrics.target + ".00",
            delta=None,
            width="content",
        )

    # Start score
    with col2:
        start_score_value = f"{device_metrics.start_score:.2f}" if device_metrics.start_score is not None else "N/A"
        st.metric(
            "**Initial Date**",
            value=start_score_value,
            delta=None,
            width="content",
        )

    # End score
    with col3:
        end_score_value = f"{device_metrics.end_score:.2f}" if device_metrics.end_score is not None else "N/A"
        delta_value = f"{device_metrics.delta:.2f}" if device_metrics.delta is not None else None
        st.metric(
            "**End Date**",
            value=end_score_value,
            delta=delta_value,
            width="content",
        )

    with col4:
        growth_rate = getattr(device_metrics, "growth_rate", None)

        if growth_rate is None:
            growth_text = "N/A"
        else:
            sign = "+" if growth_rate > 0 else ""
            growth_text = f"{sign}{growth_rate:.2f}%"

        growth_color = get_growth_color(growth_rate)

        st.markdown(f"<h2 style='margin-top:10px;color:{growth_color}'>{growth_text}</h2>", unsafe_allow_html=True)

def render_performance_section(
    mobile_metrics: DeviceMetrics,
    desktop_metrics: DeviceMetrics,
    mobile_time_series: List[TimeSeriesPoint],
    desktop_time_series: List[TimeSeriesPoint],
    filter_criteria: FilterCriteria
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
        help="The Performance Score found in tools like Google Lighthouse and PageSpeed Insights is a single 0–100 value. It is actually a weighted average of several lab metrics, including the three Core Web Vitals (LCP, CLS, and INP/TBT). " \
        "The final Performance Score is determined by assigning different weights to each metric"
    )

    # Display active filters for the performance section
    display_active_filters(filter_criteria)

    col1, col2 = st.columns(2)

    with col1.container(border=True, height="stretch"):
        st.markdown("### 📱 Mobile")
        render_device_metrics(mobile_metrics)

    with col2.container(border=True, height="stretch"):
        st.markdown("### 💻 Desktop")
        render_device_metrics(desktop_metrics)

    
    # Evolution chart
    if not mobile_time_series and not desktop_time_series:
        st.warning("No time series data available for the selected filters")
    else:
        col1 = st.container()
        with col1.container(border=True, height="stretch"):            
            fig = create_performance_evolution_chart(
                mobile_data=mobile_time_series,
                desktop_data=desktop_time_series,
            )
            st.plotly_chart(fig, use_container_width=True)

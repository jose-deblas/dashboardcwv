"""
Performance section component.

Pure rendering component that consumes view models.
No business logic or calculations - all data is pre-formatted in view models.
"""

import streamlit as st

from src.presentation.models.performance_view_model import (
    DeviceMetricsViewModel,
    PerformanceViewModel,
)
from src.presentation.models.chart_view_model import ChartViewModel
from src.dashboard.adapters.streamlit_chart_adapter import StreamlitChartAdapter


def render_device_metrics(device_vm: DeviceMetricsViewModel):
    """
    Render performance metrics for a single device.

    Pure rendering - all data pre-formatted in view model.

    Args:
        device_vm: Device metrics view model with pre-formatted values
    """
    # Check if we have data
    if not device_vm.has_data:
        st.warning(f"No data available for {device_vm.device_label}")
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

    # Target
    with col1:
        st.metric(
            "**Target**",
            value=device_vm.target_card.value,
            delta=None,
            width="content",
        )

    # Initial date score
    with col2:
        st.metric(
            "**Initial Date**",
            value=device_vm.start_date_card.value,
            delta=None,
            width="content",
        )

    # End date score
    with col3:
        st.metric(
            "**End Date**",
            value=device_vm.end_date_card.value,
            delta=device_vm.end_date_card.delta,
            width="content",
        )

    # Growth rate
    with col4:
        # Map semantic color names to hex codes
        color_map = {
            "green": "#16a34a",
            "red": "#dc2626",
            "neutral": "#6c757d",
        }
        growth_color = color_map.get(device_vm.growth_rate_color, "#6c757d")

        st.markdown(
            f"<h2 style='margin-top:10px;color:{growth_color}'>{device_vm.growth_rate_display}</h2>",
            unsafe_allow_html=True,
        )

def render_performance_section(
    performance_vm: PerformanceViewModel, chart_vm: ChartViewModel
):
    """
    Render the complete performance section.

    Pure rendering from view models - no business logic.

    Args:
        performance_vm: Complete performance view model
        chart_vm: Chart view model for performance evolution
    """

    st.markdown(
        '<h2 class="highlight">📊 Performance Score <span title="The Performance Score found in tools like Google Lighthouse and PageSpeed Insights is a single 0–100 value. It is actually a weighted average of several lab metrics, including the three Core Web Vitals (LCP, CLS, and INP/TBT). The final Performance Score is determined by assigning different weights to each metric." style="font-size:0.5em; margin-left:6px; vertical-align:middle; cursor:help;">ℹ️</span></h2>',
        unsafe_allow_html=True,
    )

    # Display active filters
    for filter_text in performance_vm.active_filters_display:
        st.info(filter_text)

    col1, col2 = st.columns(2)

    with col1.container(border=True, height="stretch"):
        st.markdown("### 📱 Mobile")
        render_device_metrics(performance_vm.mobile)

    with col2.container(border=True, height="stretch"):
        st.markdown("### 💻 Desktop")
        render_device_metrics(performance_vm.desktop)

    # Evolution chart
    if not performance_vm.has_time_series_data:
        st.warning("No time series data available for the selected filters")
    else:
        col1 = st.container()
        with col1.container(border=True, height="stretch"):
            # Convert chart VM to Plotly figure using adapter
            chart_adapter = StreamlitChartAdapter()
            fig = chart_adapter.render_chart(chart_vm)
            st.plotly_chart(fig, use_container_width=True)

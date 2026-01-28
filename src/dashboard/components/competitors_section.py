"""
Competitors section component.

Pure rendering component that consumes view models.
No business logic - medals, highlighting, and styling are pre-computed.
"""

from typing import List

import streamlit as st

from src.presentation.models.competitor_view_model import (
    RankingViewModel,
    CompetitorViewModel,
)
from src.presentation.models.chart_view_model import ChartViewModel
from src.dashboard.adapters.streamlit_chart_adapter import StreamlitChartAdapter


def render_rankings_table(rankings: List[RankingViewModel]):
    """
    Render brand rankings table.

    Pure rendering - medals and highlighting pre-computed in view model.

    Args:
        rankings: List of ranking view models
    """
    if not rankings:
        st.warning("No ranking data available")
        return

    # Render each ranking
    for ranking in rankings:
        # Highlight target brands with special styling
        if ranking.is_highlighted:
            st.markdown(
                f"""
                <div style="background-color: #2d3748; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #a7f9ab;">
                    <span style="font-size: 24px; font-weight: bold; color: #a7f9ab;"">{ranking.medal} #{ranking.rank}</span>
                    <span style="font-size: 20px; font-weight: bold; margin-left: 15px; color: #a7f9ab;">{ranking.brand}</span>
                    <span style="float: right; font-size: 24px; font-weight: bold; color: #a7f9ab;"">{ranking.score}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid;">
                    <span style="font-size: 24px; font-weight: bold;">{ranking.medal} #{ranking.rank}</span>
                    <span style="font-size: 20px; margin-left: 15px;">{ranking.brand}</span>
                    <span style="float: right; font-size: 24px; font-weight: bold;">{ranking.score}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_competitor_section(
    competitor_vm: CompetitorViewModel,
    mobile_chart_vm: ChartViewModel,
    desktop_chart_vm: ChartViewModel,
):
    """
    Render the complete competitors section.

    Pure rendering from view models - no business logic.

    Args:
        competitor_vm: Complete competitor view model
        mobile_chart_vm: Chart view model for mobile evolution
        desktop_chart_vm: Chart view model for desktop evolution
    """
    st.markdown("---")
    st.markdown(
        '<h2 class="highlight">🏆 Competitor Rankings <span title="Competitor rankings are based on the average Performance Score over the last date in the range. We take into account the selected filters to show competitors data." style="font-size:0.5em; margin-left:6px; vertical-align:middle; cursor:help;">ℹ️</span></h2>',
        unsafe_allow_html=True,
    )

    # Display active filters
    for filter_text in competitor_vm.active_filters_display:
        st.info(filter_text)

    # Mobile section
    col1, col2 = st.columns([2, 5])

    with col1.container(border=True, height="stretch"):
        st.markdown("#### 📱 Mobile Ranking")
        render_rankings_table(competitor_vm.mobile_rankings)

    with col2.container(border=True, height="stretch"):
        if competitor_vm.has_mobile_time_series:
            chart_adapter = StreamlitChartAdapter()
            fig = chart_adapter.render_chart(mobile_chart_vm)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No mobile competitor time series data available")

    # Desktop section
    col1, col2 = st.columns([2, 5])

    with col1.container(border=True, height="stretch"):
        st.markdown("#### 💻 Desktop Ranking")
        render_rankings_table(competitor_vm.desktop_rankings)

    with col2.container(border=True, height="stretch"):
        if competitor_vm.has_desktop_time_series:
            chart_adapter = StreamlitChartAdapter()
            fig = chart_adapter.render_chart(desktop_chart_vm)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No desktop competitor time series data available")

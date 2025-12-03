"""
Competitors section component.

This module provides the competitors section of the dashboard,
including rankings and evolution charts.
"""

from typing import List

import streamlit as st

from src.application.dto.dashboard_dtos import BrandRanking, CompetitorData
from src.dashboard.components.charts import create_competitor_evolution_chart


def render_rankings_table(rankings: List[BrandRanking]):
    """
    Render brand rankings table.

    Args:
        rankings: List of brand rankings
    """
    if not rankings:
        st.warning("No ranking data available")
        return

    # Create ranking display
    for ranking in rankings:
        medal = ""
        if ranking.rank == 1:
            medal = "🥇"
        elif ranking.rank == 2:
            medal = "🥈"
        elif ranking.rank == 3:
            medal = "🥉"

        # Highlight target brands
        if ranking.is_target_brand:
            st.markdown(
                f"""
                <div style="background-color: #2d3748; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #a7f9ab;">
                    <span style="font-size: 24px; font-weight: bold; color: #a7f9ab;"">{medal} #{ranking.rank}</span>
                    <span style="font-size: 20px; font-weight: bold; margin-left: 15px; color: #a7f9ab;">{ranking.brand}</span>
                    <span style="float: right; font-size: 24px; font-weight: bold; color: #a7f9ab;"">{ranking.avg_performance_score:.2f}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid;">
                    <span style="font-size: 24px; font-weight: bold;">{medal} #{ranking.rank}</span>
                    <span style="font-size: 20px; margin-left: 15px;">{ranking.brand}</span>
                    <span style="float: right; font-size: 24px; font-weight: bold;">{ranking.avg_performance_score:.2f}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_competitor_section(
    mobile_competitor_data: CompetitorData, desktop_competitor_data: CompetitorData
):
    """
    Render the complete competitors section.

    Args:
        mobile_competitor_data: Competitor data for mobile
        desktop_competitor_data: Competitor data for desktop
    """
    st.markdown("---")
    st.markdown('<h2 class="highlight">🏆 Competitor Rankings</h2>', unsafe_allow_html=True)

    # Create two columns for mobile and desktop
    col1, col2 = st.columns([2,5]) 

    with col1.container(border=True, height="stretch"):
        st.markdown("#### 📱 Mobile Ranking")
        render_rankings_table(mobile_competitor_data.rankings)

    with col2.container(border=True, height="stretch"):
        # Mobile evolution
        if mobile_competitor_data.time_series:
            # Extract target brands from rankings
            target_brands = [
                r.brand for r in mobile_competitor_data.rankings if r.is_target_brand
            ]
            fig_mobile = create_competitor_evolution_chart(
                time_series_data=mobile_competitor_data.time_series,
                device="mobile",
                target_brands=target_brands,
            )
            st.plotly_chart(fig_mobile, use_container_width=True)
        else:
            st.warning("No mobile competitor time series data available")

    col1, col2 = st.columns([2,5]) 

    with col1.container(border=True, height="stretch"):
        st.markdown("#### 💻 Desktop Ranking")
        render_rankings_table(desktop_competitor_data.rankings)

    with col2.container(border=True, height="stretch"):        
        if desktop_competitor_data.time_series:
            # Extract target brands from rankings
            target_brands = [
                r.brand for r in desktop_competitor_data.rankings if r.is_target_brand
            ]
            fig_desktop = create_competitor_evolution_chart(
                time_series_data=desktop_competitor_data.time_series,
                device="desktop",
                target_brands=target_brands,
            )
            st.plotly_chart(fig_desktop, use_container_width=True)
        else:
            st.warning("No desktop competitor time series data available")

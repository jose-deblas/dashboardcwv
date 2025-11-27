"""
Core Web Vitals Dashboard - Main Streamlit Application

This module implements the main dashboard using Streamlit with Clean Architecture.
All dependencies are injected through the DI container.
"""

import os
from datetime import date

import streamlit as st
from dotenv import load_dotenv

from src.application.dto.dashboard_dtos import FilterCriteria
from src.dashboard.components.competitors_section import render_competitor_section
from src.dashboard.components.filters import display_active_filters, render_filters
from src.dashboard.components.performance_section import render_performance_section
from src.dashboard.components.styles import get_dark_mode_css
from src.infrastructure.di.container import Container

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Core Web Vitals Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_container() -> Container:
    """
    Initialize and configure the DI container.

    Returns:
        Configured Container instance
    """
    container = Container()

    # Load configuration from environment
    container.config.database.host.from_env("MYSQL_HOST", required=True)
    container.config.database.port.from_env("MYSQL_PORT", as_=int, default=3306)
    container.config.database.name.from_env("MYSQL_DATABASE", required=True)
    container.config.database.user.from_env("MYSQL_USER", required=True)
    container.config.database.password.from_env("MYSQL_PASSWORD", required=True)

    # PageSpeed configuration (not used in dashboard but required by container)
    container.config.pagespeed.api_key.from_env("PAGESPEED_INSIGHTS_API_KEY", default="")
    container.config.pagespeed.max_retries.from_env("PAGESPEED_MAX_RETRIES", as_=int, default=3)
    container.config.pagespeed.timeout.from_env("PAGESPEED_TIMEOUT", as_=int, default=30)
    container.config.pagespeed.initial_backoff.from_env("PAGESPEED_INITIAL_BACKOFF", as_=int, default=1)
    container.config.pagespeed.backoff_multiplier.from_env("PAGESPEED_BACKOFF_MULTIPLIER", as_=int, default=2)

    return container


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "filter_criteria" not in st.session_state:
        st.session_state.filter_criteria = None
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True  # Default to dark mode


def main():
    """Main dashboard application."""
    initialize_session_state()

    # Apply dark mode CSS
    if st.session_state.dark_mode:
        st.markdown(get_dark_mode_css(), unsafe_allow_html=True)

    # Initialize DI container
    try:
        container = get_container()
    except Exception as e:
        st.error(f"Failed to initialize application: {str(e)}")
        st.stop()

    # Sidebar
    with st.sidebar:
        st.markdown('<h1 class="highlight">📊 CWV Dashboard</h1>', unsafe_allow_html=True)
        st.markdown("---")
 
        # Navigation menu with links with streamlit markdown
        st.markdown(
            """
            [Home](#)
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Dark mode toggle
        dark_mode = st.toggle("🌙 Dark Mode")
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()

    # Main content
    st.markdown('<h1 class="highlight">Core Web Vitals Dashboard</h1>', unsafe_allow_html=True)

    # Load filter options
    try:
        get_filter_options_use_case = container.get_filter_options_use_case()
        filter_options = get_filter_options_use_case.execute()

        # Check if we have data
        if filter_options.min_date is None or filter_options.max_date is None:
            st.warning(
                "⚠️ No data available in the database. "
                "Please run the data collection job first to populate the database."
            )
            st.stop()

    except Exception as e:
        st.error(f"Failed to load filter options: {str(e)}")
        st.stop()

    # Initialize default filter criteria if not set
    if st.session_state.filter_criteria is None:
        st.session_state.filter_criteria = FilterCriteria(
            start_date=filter_options.min_date,
            end_date=filter_options.max_date,
            brands=filter_options.brands,
            countries=None,
            page_types=None,
        )

    # Render filters
    new_filter_criteria = render_filters(filter_options)
    if new_filter_criteria:
        st.session_state.filter_criteria = new_filter_criteria

    st.markdown("---")

    # Display active filters
    display_active_filters(st.session_state.filter_criteria)

    # Fetch and display data
    try:
        filter_criteria = st.session_state.filter_criteria

        # Get use cases from container
        get_performance_data_use_case = container.get_performance_data_use_case()
        get_competitor_data_use_case = container.get_competitor_data_use_case()

        # Show loading spinner
        with st.spinner("Loading dashboard data..."):
            # Fetch performance data
            performance_metrics = get_performance_data_use_case.execute(filter_criteria)

            # Fetch time series for performance evolution
            mobile_time_series = get_performance_data_use_case.get_time_series(
                filter_criteria, "mobile"
            )
            desktop_time_series = get_performance_data_use_case.get_time_series(
                filter_criteria, "desktop"
            )

            # Fetch competitor data
            mobile_competitor_data = get_competitor_data_use_case.execute(
                filter_criteria, "mobile"
            )
            desktop_competitor_data = get_competitor_data_use_case.execute(
                filter_criteria, "desktop"
            )

        # Render performance section
        render_performance_section(
            mobile_metrics=performance_metrics.mobile_metrics,
            desktop_metrics=performance_metrics.desktop_metrics,
            mobile_time_series=mobile_time_series,
            desktop_time_series=desktop_time_series,
        )

        # Render competitors section
        render_competitor_section(
            mobile_competitor_data=mobile_competitor_data,
            desktop_competitor_data=desktop_competitor_data,
        )

    except Exception as e:
        st.error(f"Failed to load dashboard data: {str(e)}")
        st.exception(e)

    # Footer
    st.markdown("---")
    st.caption("Core Web Vitals Dashboard | Built with Clean Architecture principles")


if __name__ == "__main__":
    main()

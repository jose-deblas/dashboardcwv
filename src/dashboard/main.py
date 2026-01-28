"""
Core Web Vitals Dashboard - Main Streamlit Application

This module implements the main dashboard using Streamlit with Clean Architecture.
All dependencies are injected through the DI container.

Architecture:
- Uses Presentation Layer (presenters, view models) for framework-agnostic logic
- Uses Streamlit Adapters for framework-specific implementations
- Components are pure renderers that consume view models
"""

import os
from datetime import date

import streamlit as st
from dotenv import load_dotenv

from src.application.dto.dashboard_dtos import FilterCriteria
from src.application.validation.filter_validator import FilterValidator
from src.dashboard.adapters.streamlit_state_adapter import StreamlitStateAdapter
from src.dashboard.adapters.streamlit_chart_adapter import StreamlitChartAdapter
from src.dashboard.components.competitors_section import render_competitor_section
from src.dashboard.components.filters import render_filters
from src.dashboard.components.performance_section import render_performance_section
from src.infrastructure.di.container import Container
from src.presentation.presenters.performance_presenter import PerformancePresenter
from src.presentation.presenters.competitor_presenter import CompetitorPresenter
from src.presentation.presenters.filter_presenter import FilterPresenter

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

    # Chart thresholds (defaults)
    container.config.thresholds.red.from_env("THRESHOLD_RED", as_=int, default=40)
    container.config.thresholds.green.from_env("THRESHOLD_GREEN", as_=int, default=60)

    return container


def main():
    """Main dashboard application with presentation layer."""
    # Initialize DI container
    try:
        container = get_container()
    except Exception as e:
        st.error(f"Failed to initialize application: {str(e)}")
        st.stop()

    # Get framework-agnostic components
    state_adapter = StreamlitStateAdapter()
    performance_presenter = PerformancePresenter()
    competitor_presenter = CompetitorPresenter()
    filter_presenter = FilterPresenter()
    chart_builder = container.chart_builder()
    validator = FilterValidator()

    # Main content
    st.markdown('<h1 class="highlight">Core Web Vitals Dashboard</h1>', unsafe_allow_html=True)

    # Load filter options
    try:
        get_filter_options_use_case = container.get_filter_options_use_case()
        filter_options_dto = get_filter_options_use_case.execute()

        # Check if we have data
        if filter_options_dto.min_date is None or filter_options_dto.max_date is None:
            st.warning(
                "⚠️ No data available in the database. "
                "Please run the data collection job first to populate the database."
            )
            st.stop()

        # Transform to view model
        filter_options_vm = filter_presenter.present_options(filter_options_dto)

    except Exception as e:
        st.error(f"Failed to load filter options: {str(e)}")
        st.stop()

    # Initialize default filter criteria if not set
    current_criteria = state_adapter.get_filter_criteria()
    if current_criteria is None:
        current_criteria = FilterCriteria(
            start_date=filter_options_dto.min_date,
            end_date=filter_options_dto.max_date,
            brands=filter_options_dto.brands,
            countries=None,
            page_types=None,
        )
        state_adapter.set_filter_criteria(current_criteria)

    # Render filters
    with st.expander("Show/Hide Filters", expanded=False):
        new_criteria = render_filters(filter_options_vm, validator)
        if new_criteria:
            state_adapter.set_filter_criteria(new_criteria)
            current_criteria = new_criteria
    
    # Fetch and display data
    try:
        # Get use cases from container
        get_performance_data_use_case = container.get_performance_data_use_case()
        get_competitor_data_use_case = container.get_competitor_data_use_case()

        # Show loading spinner
        with st.spinner("Loading dashboard data..."):
            # Fetch DTOs (business data)
            performance_metrics = get_performance_data_use_case.execute(current_criteria)
            mobile_time_series = get_performance_data_use_case.get_time_series(
                current_criteria, "mobile"
            )
            desktop_time_series = get_performance_data_use_case.get_time_series(
                current_criteria, "desktop"
            )

            mobile_competitor_data = get_competitor_data_use_case.execute(
                current_criteria, "mobile"
            )
            desktop_competitor_data = get_competitor_data_use_case.execute(
                current_criteria, "desktop"
            )

            # Transform to view models (presentation layer)
            performance_vm = performance_presenter.present(
                performance_metrics, mobile_time_series, desktop_time_series
            )

            performance_chart_vm = chart_builder.build_performance_evolution_chart(
                mobile_time_series, desktop_time_series
            )

            competitor_vm = competitor_presenter.present(
                mobile_competitor_data, desktop_competitor_data
            )

            # Get target brands for chart styling
            target_brands = [
                r.brand
                for r in mobile_competitor_data.rankings
                if r.is_target_brand
            ]

            mobile_chart_vm = chart_builder.build_competitor_evolution_chart(
                mobile_competitor_data.time_series, "mobile", target_brands
            )

            desktop_chart_vm = chart_builder.build_competitor_evolution_chart(
                desktop_competitor_data.time_series, "desktop", target_brands
            )

        # Render (pure presentation)
        render_performance_section(performance_vm, performance_chart_vm)
        render_competitor_section(competitor_vm, mobile_chart_vm, desktop_chart_vm)

    except Exception as e:
        st.error(f"Failed to load dashboard data: {str(e)}")
        st.exception(e)

    # Footer
    st.markdown("---")

if __name__ == "__main__":
    main()

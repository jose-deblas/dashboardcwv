"""
Dashboard filter components.

This module provides the filter form for the dashboard.
"""

from datetime import date
from typing import List, Optional, Tuple

import streamlit as st

from src.application.dto.dashboard_dtos import FilterCriteria, FilterOptions


def render_filters(filter_options: FilterOptions) -> Optional[FilterCriteria]:
    """
    Render the dashboard filter form.

    Args:
        filter_options: Available filter options from the database

    Returns:
        FilterCriteria if form is submitted, None otherwise
    """

    with st.form(key="dashboard_filters"):
        col1, col2, col3, col4 = st.columns(4)

        # Date range filters
        with col1:
            start_date = st.date_input(
                "Initial Date",
                value=filter_options.min_date if filter_options.min_date else date.today(),
                min_value=filter_options.min_date,
                max_value=filter_options.max_date,
                help="Select the initial date for data analysis",
            )

        with col2:
            end_date = st.date_input(
                "End Date",
                value=filter_options.max_date if filter_options.max_date else date.today(),
                min_value=filter_options.min_date,
                max_value=filter_options.max_date,
                help="Select the end date for data analysis",
            )

        # Brand filter
        with col3:
            brand_options = ["All"] + filter_options.brands
            selected_brand = st.selectbox(
                "Brand",
                options=brand_options,
                index=0,
                help="Filter by your target brand. Option [All] means that we show the average for our target brands, all those listed in the filter",
            )

        # Country filter
        with col4:
            country_options = ["All"] + filter_options.countries
            selected_country = st.selectbox(
                "Country",
                options=country_options,
                index=0,
                help="Filter by country",
            )

        # Page type filter (multiselect)
        page_type_options = filter_options.page_types
        selected_page_types = st.multiselect(
            "Page Types",
            options=page_type_options,
            default=[],
            help="Filter by page types (leave empty for all)",
        )

        # Submit button
        submit_button = st.form_submit_button(
            label="Apply Filters",
            use_container_width=True,
            type="primary",
        )

        if submit_button:
            # Validate dates
            if start_date > end_date:
                st.error("Start date must be before or equal to end date")
                return None

            # Convert "All" selections to None (no filter) except for target brand (all target brands)
            brands = filter_options.brands if selected_brand == "All" else [selected_brand]
            countries = None if selected_country == "All" else [selected_country]
            page_types = None if not selected_page_types else selected_page_types

            return FilterCriteria(
                start_date=start_date,
                end_date=end_date,
                brands=brands,
                countries=countries,
                page_types=page_types,
            )
    
    return None


def display_active_filters(filter_criteria: FilterCriteria):
    """
    Display the currently active filters.

    Args:
        filter_criteria: Current filter criteria
    """

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info(f"📅 **From** {filter_criteria.start_date} **to** {filter_criteria.end_date}")

    with col2:
        brands_text = (
            ", ".join(filter_criteria.brands)
            if filter_criteria.brands
            else "All Brands"
        )
        st.info(f"🏢 **Brand:** {brands_text}")

    with col3:
        countries_text = (
            ", ".join(filter_criteria.countries)
            if filter_criteria.countries
            else "All Countries"
        )
        st.info(f"🌍 **Country:** {countries_text}")

    with col4:
        page_types_text = (
            ", ".join(filter_criteria.page_types)
            if filter_criteria.page_types
            else "All Page Types"
        )
        st.info(f"📄 **Page Types:** {page_types_text}")

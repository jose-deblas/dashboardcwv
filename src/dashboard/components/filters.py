"""
Dashboard filter components.

Pure rendering component for filter form.
Validation delegated to FilterValidator.
"""

from datetime import date
from typing import Optional

import streamlit as st

from src.application.dto.dashboard_dtos import FilterCriteria
from src.application.validation.filter_validator import (
    FilterValidator,
    FilterValidationError,
)
from src.presentation.models.filter_view_model import FilterOptionsViewModel


def render_filters(
    options_vm: FilterOptionsViewModel, validator: FilterValidator
) -> Optional[FilterCriteria]:
    """
    Render the dashboard filter form.

    Pure filter form rendering. Validation delegated to FilterValidator.

    Args:
        options_vm: Filter options view model
        validator: Filter validator for business rules

    Returns:
        FilterCriteria if form is submitted and valid, None otherwise
    """
    with st.form(key="dashboard_filters"):
        col1, col2, col3, col4 = st.columns(4)

        # Date range filters
        with col1:
            start_date = st.date_input(
                "Initial Date",
                value=options_vm.default_start_date,
                min_value=options_vm.min_date,
                max_value=options_vm.max_date,
                help="Select the initial date for data analysis",
            )

        with col2:
            end_date = st.date_input(
                "End Date",
                value=options_vm.default_end_date,
                min_value=options_vm.min_date,
                max_value=options_vm.max_date,
                help="Select the end date for data analysis",
            )

        # Brand filter
        with col3:
            selected_brand = st.selectbox(
                "Brand",
                options=options_vm.brand_options,
                index=0,
                help="Filter by your target brand. Option [All] means that we show the average for our target brands, all those listed in the filter",
            )

        # Country filter
        with col4:
            selected_country = st.selectbox(
                "Country",
                options=options_vm.country_options,
                index=0,
                help="Filter by country",
            )

        # Page type filter (multiselect)
        selected_page_types = st.multiselect(
            "Page Types",
            options=options_vm.page_type_options,
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
            # Validate using injected validator
            try:
                validator.validate_date_range(start_date, end_date)
            except FilterValidationError as e:
                st.error(str(e))
                return None

            # Transform selections to FilterCriteria
            # Remove "All" from brand options to get actual brands list
            all_brands = [b for b in options_vm.brand_options if b != "All"]
            brands = (
                all_brands if selected_brand == "All" else [selected_brand]
            )
            countries = (
                None if selected_country == "All" else [selected_country]
            )
            page_types = None if not selected_page_types else selected_page_types

            return FilterCriteria(
                start_date=start_date,
                end_date=end_date,
                brands=brands,
                countries=countries,
                page_types=page_types,
            )

    return None

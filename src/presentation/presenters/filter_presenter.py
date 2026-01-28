"""
Presenter for transforming filter DTOs into view models.

This presenter handles filter option formatting and selection transformation.
"""

from src.application.dto.dashboard_dtos import FilterOptions, FilterCriteria
from src.presentation.models.filter_view_model import (
    FilterOptionsViewModel,
    FilterSelectionViewModel,
)


class FilterPresenter:
    """
    Transforms filter DTOs into view models.

    Handles "All" option prefixing and selection formatting.
    """

    def present_options(
        self, options: FilterOptions
    ) -> FilterOptionsViewModel:
        """
        Transform filter options into view model.

        Args:
            options: Filter options DTO from use case

        Returns:
            Filter options view model with "All" prefixes
        """
        return FilterOptionsViewModel(
            min_date=options.min_date,
            max_date=options.max_date,
            brand_options=["All"] + options.brands,
            country_options=["All"] + options.countries,
            page_type_options=options.page_types,
            default_start_date=options.min_date,
            default_end_date=options.max_date,
        )

    def present_selection(
        self,
        criteria: FilterCriteria,
        all_brands: list[str],
        validation_error: str | None = None,
    ) -> FilterSelectionViewModel:
        """
        Transform filter selection into view model.

        Args:
            criteria: Current filter criteria
            all_brands: Complete list of available brands
            validation_error: Optional validation error message

        Returns:
            Filter selection view model
        """
        # Reverse transform brands (if all brands selected, show "All")
        if criteria.brands and len(criteria.brands) == len(all_brands):
            selected_brand = "All"
        elif criteria.brands and len(criteria.brands) == 1:
            selected_brand = criteria.brands[0]
        else:
            selected_brand = "All"

        selected_country = (
            "All"
            if criteria.countries is None
            else criteria.countries[0] if criteria.countries else "All"
        )
        selected_page_types = criteria.page_types or []

        return FilterSelectionViewModel(
            start_date=criteria.start_date,
            end_date=criteria.end_date,
            selected_brand=selected_brand,
            selected_country=selected_country,
            selected_page_types=selected_page_types,
            validation_error=validation_error,
        )

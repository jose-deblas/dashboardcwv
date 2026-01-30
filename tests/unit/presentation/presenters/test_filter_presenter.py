"""
Tests for FilterPresenter.

Tests filter option and selection transformation logic:
- "All" option prefixing
- Selection formatting
- Reverse transformation of selections
"""

from datetime import date

import pytest

from src.application.dto.dashboard_dtos import FilterOptions, FilterCriteria
from src.presentation.presenters.filter_presenter import FilterPresenter
from src.presentation.models.filter_view_model import (
    FilterOptionsViewModel,
    FilterSelectionViewModel,
)


class TestFilterPresenter:
    """Test suite for FilterPresenter."""

    @pytest.fixture
    def presenter(self):
        """Create presenter instance."""
        return FilterPresenter()

    # Test present_options
    def test_present_options_adds_all_to_brands(self, presenter):
        """Test that 'All' is prepended to brand options."""
        options = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=["Brand A", "Brand B", "Brand C"],
            countries=["US", "UK"],
            page_types=["home", "product"],
        )

        result = presenter.present_options(options)

        assert result.brand_options[0] == "All"
        assert result.brand_options[1:] == ["Brand A", "Brand B", "Brand C"]
        assert len(result.brand_options) == 4

    def test_present_options_adds_all_to_countries(self, presenter):
        """Test that 'All' is prepended to country options."""
        options = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=["Brand A"],
            countries=["US", "UK", "CA"],
            page_types=["home"],
        )

        result = presenter.present_options(options)

        assert result.country_options[0] == "All"
        assert result.country_options[1:] == ["US", "UK", "CA"]
        assert len(result.country_options) == 4

    def test_present_options_page_types_unchanged(self, presenter):
        """Test that page types are not prefixed with 'All'."""
        options = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home", "product", "category"],
        )

        result = presenter.present_options(options)

        assert result.page_type_options == ["home", "product", "category"]
        assert "All" not in result.page_type_options

    def test_present_options_date_range(self, presenter):
        """Test that date range is preserved."""
        options = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        result = presenter.present_options(options)

        assert result.min_date == date(2024, 1, 1)
        assert result.max_date == date(2024, 12, 31)
        assert result.default_start_date == date(2024, 1, 1)
        assert result.default_end_date == date(2024, 12, 31)

    def test_present_options_empty_lists(self, presenter):
        """Test with empty brand, country, and page type lists."""
        options = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=[],
            countries=[],
            page_types=[],
        )

        result = presenter.present_options(options)

        assert result.brand_options == ["All"]
        assert result.country_options == ["All"]
        assert result.page_type_options == []

    def test_present_options_single_item_lists(self, presenter):
        """Test with single item in each list."""
        options = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=["Only Brand"],
            countries=["Only Country"],
            page_types=["Only Type"],
        )

        result = presenter.present_options(options)

        assert result.brand_options == ["All", "Only Brand"]
        assert result.country_options == ["All", "Only Country"]
        assert result.page_type_options == ["Only Type"]

    def test_present_options_returns_view_model(self, presenter):
        """Test that result is FilterOptionsViewModel instance."""
        options = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        result = presenter.present_options(options)

        assert isinstance(result, FilterOptionsViewModel)

    # Test present_selection
    def test_present_selection_single_brand(self, presenter):
        """Test selection with single brand."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A", "Brand B", "Brand C"]

        result = presenter.present_selection(criteria, all_brands)

        assert result.selected_brand == "Brand A"

    def test_present_selection_all_brands(self, presenter):
        """Test selection when all brands are selected."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A", "Brand B", "Brand C"],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A", "Brand B", "Brand C"]

        result = presenter.present_selection(criteria, all_brands)

        assert result.selected_brand == "All"

    def test_present_selection_multiple_brands_not_all(self, presenter):
        """Test selection with multiple brands but not all."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A", "Brand B"],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A", "Brand B", "Brand C", "Brand D"]

        result = presenter.present_selection(criteria, all_brands)

        # Should show "All" when multiple but not all brands selected
        assert result.selected_brand == "All"

    def test_present_selection_none_brands(self, presenter):
        """Test selection with None brands."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=None,
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A", "Brand B"]

        result = presenter.present_selection(criteria, all_brands)

        # None brands should show "All"
        assert result.selected_brand == "All"

    def test_present_selection_single_country(self, presenter):
        """Test selection with single country."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A"]

        result = presenter.present_selection(criteria, all_brands)

        assert result.selected_country == "US"

    def test_present_selection_none_countries(self, presenter):
        """Test selection with None countries."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=None,
            page_types=["home"],
        )
        all_brands = ["Brand A"]

        result = presenter.present_selection(criteria, all_brands)

        assert result.selected_country == "All"

    def test_present_selection_empty_countries(self, presenter):
        """Test selection with empty countries list."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=[],
            page_types=["home"],
        )
        all_brands = ["Brand A"]

        result = presenter.present_selection(criteria, all_brands)

        assert result.selected_country == "All"

    def test_present_selection_page_types(self, presenter):
        """Test selection with page types."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home", "product"],
        )
        all_brands = ["Brand A"]

        result = presenter.present_selection(criteria, all_brands)

        assert result.selected_page_types == ["home", "product"]

    def test_present_selection_none_page_types(self, presenter):
        """Test selection with None page types."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=None,
        )
        all_brands = ["Brand A"]

        result = presenter.present_selection(criteria, all_brands)

        assert result.selected_page_types == []

    def test_present_selection_dates(self, presenter):
        """Test that dates are preserved."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 15),
            end_date=date(2024, 2, 20),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A"]

        result = presenter.present_selection(criteria, all_brands)

        assert result.start_date == date(2024, 1, 15)
        assert result.end_date == date(2024, 2, 20)

    def test_present_selection_with_validation_error(self, presenter):
        """Test selection with validation error."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A"]
        error_msg = "Start date must be before end date"

        result = presenter.present_selection(criteria, all_brands, error_msg)

        assert result.validation_error == error_msg

    def test_present_selection_without_validation_error(self, presenter):
        """Test selection without validation error."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A"]

        result = presenter.present_selection(criteria, all_brands)

        assert result.validation_error is None

    def test_present_selection_returns_view_model(self, presenter):
        """Test that result is FilterSelectionViewModel instance."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A"]

        result = presenter.present_selection(criteria, all_brands)

        assert isinstance(result, FilterSelectionViewModel)


class TestFilterPresenterEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def presenter(self):
        """Create presenter instance."""
        return FilterPresenter()

    def test_present_options_many_brands(self, presenter):
        """Test with many brands."""
        brands = [f"Brand {i}" for i in range(1, 51)]
        options = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=brands,
            countries=["US"],
            page_types=["home"],
        )

        result = presenter.present_options(options)

        assert len(result.brand_options) == 51  # 50 brands + "All"
        assert result.brand_options[0] == "All"

    def test_present_selection_empty_brands_list(self, presenter):
        """Test selection with empty brands list."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=[],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A", "Brand B"]

        result = presenter.present_selection(criteria, all_brands)

        assert result.selected_brand == "All"

    def test_present_selection_brand_not_in_all_brands(self, presenter):
        """Test selection when selected brand not in all_brands list."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand X"],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A", "Brand B"]

        result = presenter.present_selection(criteria, all_brands)

        # Should still work and return the brand
        assert result.selected_brand == "Brand X"

    def test_present_options_duplicate_brands(self, presenter):
        """Test with duplicate brands in list."""
        options = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=["Brand A", "Brand A", "Brand B"],
            countries=["US"],
            page_types=["home"],
        )

        result = presenter.present_options(options)

        # Should preserve duplicates (presenter doesn't deduplicate)
        assert result.brand_options == ["All", "Brand A", "Brand A", "Brand B"]

    def test_present_selection_same_start_end_date(self, presenter):
        """Test selection with same start and end date."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 1),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = ["Brand A"]

        result = presenter.present_selection(criteria, all_brands)

        assert result.start_date == result.end_date
        assert result.start_date == date(2024, 1, 1)

    def test_present_options_leap_year_dates(self, presenter):
        """Test with leap year date range."""
        options = FilterOptions(
            min_date=date(2024, 2, 1),
            max_date=date(2024, 2, 29),  # Leap year
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        result = presenter.present_options(options)

        assert result.min_date == date(2024, 2, 1)
        assert result.max_date == date(2024, 2, 29)

    def test_present_selection_all_brands_empty_list(self, presenter):
        """Test selection when all_brands is empty."""
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )
        all_brands = []

        result = presenter.present_selection(criteria, all_brands)

        # Should show the single brand since len(criteria.brands) == 1
        assert result.selected_brand == "Brand A"

    def test_present_options_special_characters_in_names(self, presenter):
        """Test with special characters in brand/country names."""
        options = FilterOptions(
            min_date=date(2024, 1, 1),
            max_date=date(2024, 12, 31),
            brands=["Brand & Co.", "Brand's Shop", "Brand (TM)"],
            countries=["U.S.A.", "U.K."],
            page_types=["home-page", "product_detail"],
        )

        result = presenter.present_options(options)

        assert "Brand & Co." in result.brand_options
        assert "Brand's Shop" in result.brand_options
        assert "Brand (TM)" in result.brand_options
        assert "U.S.A." in result.country_options

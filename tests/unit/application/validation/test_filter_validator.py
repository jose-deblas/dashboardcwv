"""
Tests for FilterValidator.

Tests business validation rules for filter criteria:
- Date range validation
- Date boundary validation
- Error messages
"""

from datetime import date

import pytest

from src.application.validation.filter_validator import (
    FilterValidator,
    FilterValidationError,
)


class TestFilterValidatorDateRange:
    """Test suite for validate_date_range method."""

    def test_valid_date_range(self):
        """Test that valid date range passes validation."""
        validator = FilterValidator()

        # Should not raise exception
        validator.validate_date_range(date(2024, 1, 1), date(2024, 12, 31))

    def test_same_start_and_end_date(self):
        """Test that same start and end date is valid."""
        validator = FilterValidator()

        # Should not raise exception
        validator.validate_date_range(date(2024, 1, 1), date(2024, 1, 1))

    def test_consecutive_dates(self):
        """Test consecutive dates."""
        validator = FilterValidator()

        # Should not raise exception
        validator.validate_date_range(date(2024, 1, 1), date(2024, 1, 2))

    def test_invalid_date_range_raises_error(self):
        """Test that start_date > end_date raises error."""
        validator = FilterValidator()

        with pytest.raises(FilterValidationError) as exc_info:
            validator.validate_date_range(date(2024, 12, 31), date(2024, 1, 1))

        assert "Start date must be before or equal to end date" in str(
            exc_info.value
        )

    def test_invalid_date_range_one_day_apart(self):
        """Test that reversed consecutive dates raise error."""
        validator = FilterValidator()

        with pytest.raises(FilterValidationError) as exc_info:
            validator.validate_date_range(date(2024, 1, 2), date(2024, 1, 1))

        assert "Start date must be before or equal to end date" in str(
            exc_info.value
        )

    def test_year_boundary_valid_range(self):
        """Test date range across year boundary."""
        validator = FilterValidator()

        # Should not raise exception
        validator.validate_date_range(date(2023, 12, 31), date(2024, 1, 1))

    def test_multi_year_range(self):
        """Test date range across multiple years."""
        validator = FilterValidator()

        # Should not raise exception
        validator.validate_date_range(date(2020, 1, 1), date(2024, 12, 31))

    def test_leap_year_february_range(self):
        """Test date range in leap year February."""
        validator = FilterValidator()

        # Should not raise exception
        validator.validate_date_range(date(2024, 2, 1), date(2024, 2, 29))

    def test_error_is_value_error_subclass(self):
        """Test that FilterValidationError is ValueError subclass."""
        validator = FilterValidator()

        with pytest.raises(ValueError):
            validator.validate_date_range(date(2024, 12, 31), date(2024, 1, 1))


class TestFilterValidatorDateWithinRange:
    """Test suite for validate_date_within_range method."""

    def test_date_within_range(self):
        """Test date within valid range."""
        validator = FilterValidator()

        # Should not raise exception
        validator.validate_date_within_range(
            date(2024, 6, 15), date(2024, 1, 1), date(2024, 12, 31)
        )

    def test_date_equals_min_date(self):
        """Test date equal to minimum date is valid."""
        validator = FilterValidator()

        # Should not raise exception
        validator.validate_date_within_range(
            date(2024, 1, 1), date(2024, 1, 1), date(2024, 12, 31)
        )

    def test_date_equals_max_date(self):
        """Test date equal to maximum date is valid."""
        validator = FilterValidator()

        # Should not raise exception
        validator.validate_date_within_range(
            date(2024, 12, 31), date(2024, 1, 1), date(2024, 12, 31)
        )

    def test_date_before_min_date_raises_error(self):
        """Test date before minimum raises error."""
        validator = FilterValidator()

        with pytest.raises(FilterValidationError) as exc_info:
            validator.validate_date_within_range(
                date(2023, 12, 31), date(2024, 1, 1), date(2024, 12, 31)
            )

        assert "is before minimum date" in str(exc_info.value)
        assert "2023-12-31" in str(exc_info.value)
        assert "2024-01-01" in str(exc_info.value)

    def test_date_after_max_date_raises_error(self):
        """Test date after maximum raises error."""
        validator = FilterValidator()

        with pytest.raises(FilterValidationError) as exc_info:
            validator.validate_date_within_range(
                date(2025, 1, 1), date(2024, 1, 1), date(2024, 12, 31)
            )

        assert "is after maximum date" in str(exc_info.value)
        assert "2025-01-01" in str(exc_info.value)
        assert "2024-12-31" in str(exc_info.value)

    def test_none_min_date_no_lower_bound(self):
        """Test None min_date means no lower bound."""
        validator = FilterValidator()

        # Should not raise exception even with very old date
        validator.validate_date_within_range(
            date(1900, 1, 1), None, date(2024, 12, 31)
        )

    def test_none_max_date_no_upper_bound(self):
        """Test None max_date means no upper bound."""
        validator = FilterValidator()

        # Should not raise exception even with future date
        validator.validate_date_within_range(
            date(2100, 12, 31), date(2024, 1, 1), None
        )

    def test_both_bounds_none(self):
        """Test both min and max None means no bounds."""
        validator = FilterValidator()

        # Should not raise exception with any date
        validator.validate_date_within_range(date(2024, 6, 15), None, None)
        validator.validate_date_within_range(date(1900, 1, 1), None, None)
        validator.validate_date_within_range(date(2100, 12, 31), None, None)

    def test_one_day_before_min(self):
        """Test date one day before minimum."""
        validator = FilterValidator()

        with pytest.raises(FilterValidationError):
            validator.validate_date_within_range(
                date(2024, 1, 31), date(2024, 2, 1), date(2024, 12, 31)
            )

    def test_one_day_after_max(self):
        """Test date one day after maximum."""
        validator = FilterValidator()

        with pytest.raises(FilterValidationError):
            validator.validate_date_within_range(
                date(2024, 2, 1), date(2024, 1, 1), date(2024, 1, 31)
            )

    def test_leap_year_date_validation(self):
        """Test validation with leap year date."""
        validator = FilterValidator()

        # Feb 29 should be valid in leap year
        validator.validate_date_within_range(
            date(2024, 2, 29), date(2024, 1, 1), date(2024, 12, 31)
        )


class TestFilterValidatorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_large_date_range(self):
        """Test validation with very large date range."""
        validator = FilterValidator()

        # Should not raise exception
        validator.validate_date_range(date(2000, 1, 1), date(2099, 12, 31))

    def test_date_within_very_large_range(self):
        """Test date within very large range."""
        validator = FilterValidator()

        # Should not raise exception
        validator.validate_date_within_range(
            date(2024, 6, 15), date(1900, 1, 1), date(2100, 12, 31)
        )

    def test_month_boundary_dates(self):
        """Test dates on month boundaries."""
        validator = FilterValidator()

        # Last day of month to first day of next month
        validator.validate_date_range(date(2024, 1, 31), date(2024, 2, 1))

        # First day to last day of month
        validator.validate_date_range(date(2024, 2, 1), date(2024, 2, 29))

    def test_validator_can_be_used_as_static_method(self):
        """Test that validator methods can be called as static methods."""
        # Without creating instance
        FilterValidator.validate_date_range(date(2024, 1, 1), date(2024, 12, 31))
        FilterValidator.validate_date_within_range(
            date(2024, 6, 15), date(2024, 1, 1), date(2024, 12, 31)
        )

    def test_multiple_validations_in_sequence(self):
        """Test multiple validation calls in sequence."""
        validator = FilterValidator()

        # All should pass
        validator.validate_date_range(date(2024, 1, 1), date(2024, 6, 30))
        validator.validate_date_within_range(
            date(2024, 3, 15), date(2024, 1, 1), date(2024, 12, 31)
        )
        validator.validate_date_range(date(2024, 7, 1), date(2024, 12, 31))

    def test_error_message_format_before_min(self):
        """Test error message format for date before min."""
        validator = FilterValidator()

        with pytest.raises(FilterValidationError) as exc_info:
            validator.validate_date_within_range(
                date(2023, 6, 15), date(2024, 1, 1), date(2024, 12, 31)
            )

        error_msg = str(exc_info.value)
        assert "2023-06-15" in error_msg
        assert "before" in error_msg.lower()
        assert "2024-01-01" in error_msg

    def test_error_message_format_after_max(self):
        """Test error message format for date after max."""
        validator = FilterValidator()

        with pytest.raises(FilterValidationError) as exc_info:
            validator.validate_date_within_range(
                date(2025, 6, 15), date(2024, 1, 1), date(2024, 12, 31)
            )

        error_msg = str(exc_info.value)
        assert "2025-06-15" in error_msg
        assert "after" in error_msg.lower()
        assert "2024-12-31" in error_msg


class TestFilterValidatorIntegration:
    """Integration tests for combined validation scenarios."""

    def test_validate_complete_date_range_scenario(self):
        """Test complete scenario: validate range and both dates within bounds."""
        validator = FilterValidator()
        min_available = date(2024, 1, 1)
        max_available = date(2024, 12, 31)
        start_date = date(2024, 3, 1)
        end_date = date(2024, 9, 30)

        # All validations should pass
        validator.validate_date_range(start_date, end_date)
        validator.validate_date_within_range(start_date, min_available, max_available)
        validator.validate_date_within_range(end_date, min_available, max_available)

    def test_validate_invalid_range_and_within_bounds(self):
        """Test scenario where range is invalid but dates are within bounds."""
        validator = FilterValidator()
        min_available = date(2024, 1, 1)
        max_available = date(2024, 12, 31)
        start_date = date(2024, 9, 30)
        end_date = date(2024, 3, 1)

        # Range validation should fail
        with pytest.raises(FilterValidationError):
            validator.validate_date_range(start_date, end_date)

        # But individual date bounds should pass
        validator.validate_date_within_range(start_date, min_available, max_available)
        validator.validate_date_within_range(end_date, min_available, max_available)

    def test_validate_valid_range_but_start_out_of_bounds(self):
        """Test scenario where range is valid but start date out of bounds."""
        validator = FilterValidator()
        min_available = date(2024, 1, 1)
        max_available = date(2024, 12, 31)
        start_date = date(2023, 11, 1)
        end_date = date(2024, 9, 30)

        # Range validation should pass
        validator.validate_date_range(start_date, end_date)

        # But start date bounds should fail
        with pytest.raises(FilterValidationError):
            validator.validate_date_within_range(
                start_date, min_available, max_available
            )

        # End date bounds should pass
        validator.validate_date_within_range(end_date, min_available, max_available)

    def test_exception_inheritance(self):
        """Test that FilterValidationError can be caught as ValueError."""
        validator = FilterValidator()

        # Can catch as FilterValidationError
        with pytest.raises(FilterValidationError):
            validator.validate_date_range(date(2024, 12, 31), date(2024, 1, 1))

        # Can also catch as ValueError
        with pytest.raises(ValueError):
            validator.validate_date_range(date(2024, 12, 31), date(2024, 1, 1))

    def test_error_can_be_caught_and_re_raised(self):
        """Test that errors can be caught, inspected, and re-raised."""
        validator = FilterValidator()

        try:
            validator.validate_date_range(date(2024, 12, 31), date(2024, 1, 1))
            pytest.fail("Should have raised FilterValidationError")
        except FilterValidationError as e:
            # Can inspect the error
            assert "Start date must be before or equal to end date" in str(e)
            # Can re-raise
            with pytest.raises(FilterValidationError):
                raise e

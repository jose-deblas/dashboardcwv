"""
Business validation for filter criteria.

Extracted from presentation layer and DTO __post_init__ methods.
Provides clear validation rules that can be tested independently.
"""

from datetime import date
from typing import Optional


class FilterValidationError(ValueError):
    """
    Raised when filter validation fails.

    This is a business validation error, not a presentation error.
    """

    pass


class FilterValidator:
    """
    Validates filter criteria according to business rules.

    Replaces validation logic previously in:
    - FilterCriteria.__post_init__ (DTO validation)
    - render_filters component (presentation validation)
    """

    @staticmethod
    def validate_date_range(start_date: date, end_date: date) -> None:
        """
        Validate that date range is valid.

        Args:
            start_date: Start date
            end_date: End date

        Raises:
            FilterValidationError: If start_date > end_date

        Example:
            >>> validator = FilterValidator()
            >>> validator.validate_date_range(date(2024, 1, 1), date(2024, 12, 31))
            >>> # Passes validation
            >>> validator.validate_date_range(date(2024, 12, 31), date(2024, 1, 1))
            FilterValidationError: Start date must be before or equal to end date
        """
        if start_date > end_date:
            raise FilterValidationError(
                "Start date must be before or equal to end date"
            )

    @staticmethod
    def validate_date_within_range(
        date_to_check: date,
        min_date: Optional[date],
        max_date: Optional[date],
    ) -> None:
        """
        Validate that a date is within available range.

        Args:
            date_to_check: Date to validate
            min_date: Minimum allowed date (None = no limit)
            max_date: Maximum allowed date (None = no limit)

        Raises:
            FilterValidationError: If date is out of range

        Example:
            >>> validator = FilterValidator()
            >>> validator.validate_date_within_range(
            ...     date(2024, 6, 1),
            ...     date(2024, 1, 1),
            ...     date(2024, 12, 31)
            ... )
            >>> # Passes validation
        """
        if min_date and date_to_check < min_date:
            raise FilterValidationError(
                f"Date {date_to_check} is before minimum date {min_date}"
            )
        if max_date and date_to_check > max_date:
            raise FilterValidationError(
                f"Date {date_to_check} is after maximum date {max_date}"
            )

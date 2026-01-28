"""
View models for filter section.

Framework-agnostic filter option and selection data structures.
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass(frozen=True)
class FilterOptionsViewModel:
    """
    View model for available filter options.

    Contains all available filter values with "All" prefix options
    where applicable, ready for display in UI components.
    """

    min_date: date
    max_date: date
    brand_options: List[str]  # Includes "All" as first option
    country_options: List[str]  # Includes "All" as first option
    page_type_options: List[str]
    default_start_date: date
    default_end_date: date


@dataclass(frozen=True)
class FilterSelectionViewModel:
    """
    View model for user's filter selection.

    Represents the current filter state with optional validation error.
    """

    start_date: date
    end_date: date
    selected_brand: str  # Single brand or "All"
    selected_country: str  # Single country or "All"
    selected_page_types: List[str]
    validation_error: Optional[str] = None

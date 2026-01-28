"""
Abstract state management for dashboard.

Provides a framework-agnostic interface for state management that can be
implemented by different frontends (Streamlit, Flask, React, etc.).
"""

from abc import ABC, abstractmethod
from typing import Optional

from src.application.dto.dashboard_dtos import FilterCriteria


class DashboardState(ABC):
    """
    Abstract interface for dashboard state management.

    Different frontends implement this interface to provide
    their own state storage mechanism:
    - Streamlit: st.session_state
    - Flask: session
    - React: useState/Redux
    - REST API: JWT tokens/session storage
    """

    @abstractmethod
    def get_filter_criteria(self) -> Optional[FilterCriteria]:
        """
        Get current filter criteria from state.

        Returns:
            Current filter criteria or None if not set
        """
        pass

    @abstractmethod
    def set_filter_criteria(self, criteria: FilterCriteria) -> None:
        """
        Save filter criteria to state.

        Args:
            criteria: Filter criteria to save
        """
        pass

    @abstractmethod
    def clear_state(self) -> None:
        """Clear all state."""
        pass

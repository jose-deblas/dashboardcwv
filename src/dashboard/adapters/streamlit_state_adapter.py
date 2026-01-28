"""
Streamlit-specific implementation of state management.

Wraps st.session_state to provide framework-agnostic interface.
"""

import streamlit as st
from typing import Optional

from src.application.dto.dashboard_dtos import FilterCriteria
from src.presentation.state.dashboard_state import DashboardState


class StreamlitStateAdapter(DashboardState):
    """
    Adapts Streamlit session state to DashboardState interface.

    This adapter allows Streamlit-specific state management to be used
    through the framework-agnostic DashboardState interface.

    Example:
        >>> state = StreamlitStateAdapter()
        >>> criteria = FilterCriteria(...)
        >>> state.set_filter_criteria(criteria)
        >>> retrieved = state.get_filter_criteria()
    """

    _FILTER_KEY = "filter_criteria"

    def get_filter_criteria(self) -> Optional[FilterCriteria]:
        """
        Get filter criteria from Streamlit session state.

        Returns:
            Current filter criteria or None if not set
        """
        return st.session_state.get(self._FILTER_KEY, None)

    def set_filter_criteria(self, criteria: FilterCriteria) -> None:
        """
        Save filter criteria to Streamlit session state.

        Args:
            criteria: Filter criteria to save
        """
        st.session_state[self._FILTER_KEY] = criteria

    def clear_state(self) -> None:
        """Clear filter criteria from Streamlit session state."""
        if self._FILTER_KEY in st.session_state:
            del st.session_state[self._FILTER_KEY]

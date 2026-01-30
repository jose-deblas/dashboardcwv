"""
Tests for StreamlitStateAdapter.

Tests Streamlit-specific state management adapter:
- Getting filter criteria from session state
- Setting filter criteria to session state
- Clearing state
"""

from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from src.application.dto.dashboard_dtos import FilterCriteria
from src.dashboard.adapters.streamlit_state_adapter import StreamlitStateAdapter


class TestStreamlitStateAdapter:
    """Test suite for StreamlitStateAdapter."""

    @pytest.fixture
    def mock_session_state(self):
        """Mock Streamlit session state."""
        with patch("src.dashboard.adapters.streamlit_state_adapter.st") as mock_st:
            # Create a dict-like mock for session_state
            mock_st.session_state = {}
            yield mock_st.session_state

    @pytest.fixture
    def sample_criteria(self):
        """Create sample filter criteria."""
        return FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

    # Test get_filter_criteria
    def test_get_filter_criteria_when_set(
        self, mock_session_state, sample_criteria
    ):
        """Test getting filter criteria when it exists in session state."""
        adapter = StreamlitStateAdapter()
        mock_session_state["filter_criteria"] = sample_criteria

        result = adapter.get_filter_criteria()

        assert result == sample_criteria

    def test_get_filter_criteria_when_not_set(self, mock_session_state):
        """Test getting filter criteria when not in session state returns None."""
        adapter = StreamlitStateAdapter()

        result = adapter.get_filter_criteria()

        assert result is None

    def test_get_filter_criteria_uses_correct_key(self, mock_session_state, sample_criteria):
        """Test that adapter uses correct session state key."""
        adapter = StreamlitStateAdapter()
        # Store with wrong key
        mock_session_state["wrong_key"] = sample_criteria

        result = adapter.get_filter_criteria()

        # Should not find it with wrong key
        assert result is None

    # Test set_filter_criteria
    def test_set_filter_criteria(self, mock_session_state, sample_criteria):
        """Test setting filter criteria to session state."""
        adapter = StreamlitStateAdapter()

        adapter.set_filter_criteria(sample_criteria)

        assert "filter_criteria" in mock_session_state
        assert mock_session_state["filter_criteria"] == sample_criteria

    def test_set_filter_criteria_overwrites_existing(
        self, mock_session_state, sample_criteria
    ):
        """Test that setting criteria overwrites existing value."""
        adapter = StreamlitStateAdapter()

        # Set initial criteria
        old_criteria = FilterCriteria(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
            brands=["Old Brand"],
            countries=None,
            page_types=None,
        )
        mock_session_state["filter_criteria"] = old_criteria

        # Set new criteria
        adapter.set_filter_criteria(sample_criteria)

        assert mock_session_state["filter_criteria"] == sample_criteria
        assert mock_session_state["filter_criteria"] != old_criteria

    def test_set_then_get_criteria(self, mock_session_state, sample_criteria):
        """Test setting criteria and then getting it back."""
        adapter = StreamlitStateAdapter()

        adapter.set_filter_criteria(sample_criteria)
        result = adapter.get_filter_criteria()

        assert result == sample_criteria

    # Test clear_state
    def test_clear_state_when_exists(self, mock_session_state, sample_criteria):
        """Test clearing state when criteria exists."""
        adapter = StreamlitStateAdapter()
        mock_session_state["filter_criteria"] = sample_criteria

        adapter.clear_state()

        assert "filter_criteria" not in mock_session_state

    def test_clear_state_when_not_exists(self, mock_session_state):
        """Test clearing state when criteria doesn't exist (should not error)."""
        adapter = StreamlitStateAdapter()

        # Should not raise exception
        adapter.clear_state()

        assert "filter_criteria" not in mock_session_state

    def test_clear_state_then_get_returns_none(
        self, mock_session_state, sample_criteria
    ):
        """Test that getting criteria after clear returns None."""
        adapter = StreamlitStateAdapter()
        mock_session_state["filter_criteria"] = sample_criteria

        adapter.clear_state()
        result = adapter.get_filter_criteria()

        assert result is None

    # Test DashboardState interface compliance
    def test_adapter_implements_dashboard_state_interface(self):
        """Test that adapter implements DashboardState interface."""
        from src.presentation.state.dashboard_state import DashboardState

        adapter = StreamlitStateAdapter()

        assert isinstance(adapter, DashboardState)
        assert hasattr(adapter, "get_filter_criteria")
        assert hasattr(adapter, "set_filter_criteria")
        assert hasattr(adapter, "clear_state")

    # Test with different criteria variations
    def test_set_criteria_with_none_values(self, mock_session_state):
        """Test setting criteria with None values."""
        adapter = StreamlitStateAdapter()
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=None,
            countries=None,
            page_types=None,
        )

        adapter.set_filter_criteria(criteria)
        result = adapter.get_filter_criteria()

        assert result == criteria
        assert result.brands is None
        assert result.countries is None
        assert result.page_types is None

    def test_set_criteria_with_multiple_brands(self, mock_session_state):
        """Test setting criteria with multiple brands."""
        adapter = StreamlitStateAdapter()
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A", "Brand B", "Brand C"],
            countries=["US"],
            page_types=["home", "product"],
        )

        adapter.set_filter_criteria(criteria)
        result = adapter.get_filter_criteria()

        assert result == criteria
        assert len(result.brands) == 3

    def test_set_criteria_with_same_start_end_date(self, mock_session_state):
        """Test setting criteria with same start and end date."""
        adapter = StreamlitStateAdapter()
        criteria = FilterCriteria(
            start_date=date(2024, 1, 15),
            end_date=date(2024, 1, 15),
            brands=["Brand A"],
            countries=["US"],
            page_types=None,
        )

        adapter.set_filter_criteria(criteria)
        result = adapter.get_filter_criteria()

        assert result == criteria
        assert result.start_date == result.end_date


class TestStreamlitStateAdapterEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def mock_session_state(self):
        """Mock Streamlit session state."""
        with patch("src.dashboard.adapters.streamlit_state_adapter.st") as mock_st:
            mock_st.session_state = {}
            yield mock_st.session_state

    def test_multiple_set_operations(self, mock_session_state):
        """Test multiple consecutive set operations."""
        adapter = StreamlitStateAdapter()

        criteria1 = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        criteria2 = FilterCriteria(
            start_date=date(2024, 2, 1),
            end_date=date(2024, 2, 28),
            brands=["Brand B"],
            countries=["UK"],
            page_types=["product"],
        )

        adapter.set_filter_criteria(criteria1)
        adapter.set_filter_criteria(criteria2)
        result = adapter.get_filter_criteria()

        # Should have the second criteria
        assert result == criteria2

    def test_multiple_clear_operations(self, mock_session_state):
        """Test multiple consecutive clear operations."""
        adapter = StreamlitStateAdapter()
        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        adapter.set_filter_criteria(criteria)
        adapter.clear_state()
        adapter.clear_state()  # Should not error

        result = adapter.get_filter_criteria()
        assert result is None

    def test_set_clear_set_cycle(self, mock_session_state):
        """Test set-clear-set cycle."""
        adapter = StreamlitStateAdapter()

        criteria1 = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        criteria2 = FilterCriteria(
            start_date=date(2024, 2, 1),
            end_date=date(2024, 2, 28),
            brands=["Brand B"],
            countries=["UK"],
            page_types=["product"],
        )

        adapter.set_filter_criteria(criteria1)
        assert adapter.get_filter_criteria() == criteria1

        adapter.clear_state()
        assert adapter.get_filter_criteria() is None

        adapter.set_filter_criteria(criteria2)
        assert adapter.get_filter_criteria() == criteria2

    def test_adapter_key_constant(self):
        """Test that adapter uses consistent key constant."""
        adapter = StreamlitStateAdapter()

        # The key should be accessible as class attribute
        assert hasattr(adapter, "_FILTER_KEY")
        assert adapter._FILTER_KEY == "filter_criteria"

    def test_session_state_isolation(self, mock_session_state):
        """Test that adapter only affects its own key in session state."""
        adapter = StreamlitStateAdapter()

        # Add other keys to session state
        mock_session_state["other_key"] = "other_value"
        mock_session_state["another_key"] = {"data": "value"}

        criteria = FilterCriteria(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            brands=["Brand A"],
            countries=["US"],
            page_types=["home"],
        )

        adapter.set_filter_criteria(criteria)

        # Other keys should be unaffected
        assert mock_session_state["other_key"] == "other_value"
        assert mock_session_state["another_key"] == {"data": "value"}

        adapter.clear_state()

        # Other keys should still be there
        assert mock_session_state["other_key"] == "other_value"
        assert mock_session_state["another_key"] == {"data": "value"}

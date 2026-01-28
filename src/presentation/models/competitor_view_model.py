"""
View models for competitor section.

Framework-agnostic competitor ranking and comparison data structures.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RankingViewModel:
    """
    View model for a single brand ranking.

    Contains all display data including pre-computed medal emoji
    and highlighting flag for target brands.
    """

    rank: int
    brand: str
    score: str  # Pre-formatted: "75.23"
    medal: str  # Emoji: "🥇", "🥈", "🥉", or ""
    is_highlighted: bool  # True for target brands


@dataclass(frozen=True)
class CompetitorViewModel:
    """
    Complete view model for competitor section.

    Contains rankings and time series availability for both
    mobile and desktop devices.
    """

    mobile_rankings: List[RankingViewModel]
    desktop_rankings: List[RankingViewModel]
    has_mobile_time_series: bool
    has_desktop_time_series: bool
    active_filters_display: List[str]  # Pre-formatted filter strings

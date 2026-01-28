"""
Presenter for transforming competitor DTOs into view models.

This presenter handles all presentation logic for competitor rankings including:
- Medal assignment (🥇🥈🥉)
- Highlighting target brands
- Score formatting
"""

from typing import List

from src.application.dto.dashboard_dtos import (
    CompetitorData,
    BrandRanking,
    FilterCriteria,
)
from src.presentation.models.competitor_view_model import (
    CompetitorViewModel,
    RankingViewModel,
)


class CompetitorPresenter:
    """
    Transforms competitor DTOs into view models.

    Handles medal assignment and brand highlighting logic.
    """

    def present(
        self, mobile_data: CompetitorData, desktop_data: CompetitorData
    ) -> CompetitorViewModel:
        """
        Transform competitor data into view model.

        Args:
            mobile_data: Mobile competitor data DTO
            desktop_data: Desktop competitor data DTO

        Returns:
            Complete competitor view model ready for rendering
        """
        mobile_rankings = [
            self._present_ranking(r) for r in mobile_data.rankings
        ]

        desktop_rankings = [
            self._present_ranking(r) for r in desktop_data.rankings
        ]

        active_filters = self._format_active_filters(
            mobile_data.filter_criteria
        )

        return CompetitorViewModel(
            mobile_rankings=mobile_rankings,
            desktop_rankings=desktop_rankings,
            has_mobile_time_series=bool(mobile_data.time_series),
            has_desktop_time_series=bool(desktop_data.time_series),
            active_filters_display=active_filters,
        )

    def _present_ranking(self, ranking: BrandRanking) -> RankingViewModel:
        """
        Transform single ranking with medal and highlighting.

        Args:
            ranking: Brand ranking DTO

        Returns:
            Ranking view model with medal emoji and formatting
        """
        # Assign medal emoji based on rank
        medal = ""
        if ranking.rank == 1:
            medal = "🥇"
        elif ranking.rank == 2:
            medal = "🥈"
        elif ranking.rank == 3:
            medal = "🥉"

        return RankingViewModel(
            rank=ranking.rank,
            brand=ranking.brand,
            score=f"{ranking.avg_performance_score:.2f}",
            medal=medal,
            is_highlighted=ranking.is_target_brand,
        )

    def _format_active_filters(self, criteria: FilterCriteria) -> List[str]:
        """
        Format filter criteria for display.

        Args:
            criteria: Filter criteria DTO

        Returns:
            List of formatted filter strings
        """
        filters = []

        # Date range
        filters.append(f"From {criteria.start_date} to {criteria.end_date}")

        # Brands
        if criteria.brands:
            brands = ", ".join(criteria.brands)
        else:
            brands = "All Brands"
        filters.append(f"Brand: {brands}")

        # Countries
        if criteria.countries:
            countries = ", ".join(criteria.countries)
        else:
            countries = "All Countries"
        filters.append(f"Country: {countries}")

        # Page types
        if criteria.page_types:
            page_types = ", ".join(criteria.page_types)
        else:
            page_types = "All Page Types"
        filters.append(f"Page Types: {page_types}")

        return filters

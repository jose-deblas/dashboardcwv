"""Mapper to convert PageSpeed API responses to domain entities."""
from datetime import date

from src.domain.entities.core_web_vitals import CoreWebVitals
from src.infrastructure.api.pagespeed.dto.pagespeed_response import (
    PageSpeedInsightsResponse,
)


class PageSpeedMapper:
    """Maps PageSpeed API DTO to domain entities."""

    @staticmethod
    def to_core_web_vitals(
        url_id: int,
        execution_date: date,
        response: PageSpeedInsightsResponse
    ) -> CoreWebVitals:
        """
        Convert PageSpeed API response to CoreWebVitals entity.

        Args:
            url_id: URL identifier
            execution_date: Date of execution
            response: PageSpeed Insights API response DTO

        Returns:
            CoreWebVitals domain entity
        """
        return CoreWebVitals(
            url_id=url_id,
            execution_date=execution_date,
            performance_score=response.performance_score,
            first_contentful_paint=response.first_contentful_paint,
            largest_contentful_paint=response.largest_contentful_paint,
            total_blocking_time=response.total_blocking_time,
            cumulative_layout_shift=response.cumulative_layout_shift,
            speed_index=response.speed_index,
            time_to_first_byte=response.time_to_first_byte,
            time_to_interactive=response.time_to_interactive,
            crux_largest_contentful_paint=response.crux_largest_contentful_paint,
            crux_interaction_to_next_paint=response.crux_interaction_to_next_paint,
            crux_cumulative_layout_shift=response.crux_cumulative_layout_shift,
            crux_first_contentful_paint=response.crux_first_contentful_paint,
            crux_time_to_first_byte=response.crux_time_to_first_byte,
        )

"""Tests for PageSpeed mapper."""
import pytest
from datetime import date

from src.infrastructure.api.pagespeed.dto.pagespeed_response import (
    PageSpeedInsightsResponse,
)
from src.infrastructure.api.pagespeed.mappers.pagespeed_mapper import PageSpeedMapper
from src.domain.entities.core_web_vitals import CoreWebVitals


class TestPageSpeedMapper:
    """Test suite for PageSpeedMapper."""

    def test_to_core_web_vitals_maps_all_fields(
        self, sample_pagespeed_response, sample_execution_date
    ):
        """Test that mapper correctly maps all fields from DTO to entity."""
        # Arrange
        url_id = 123
        response_dto = PageSpeedInsightsResponse(sample_pagespeed_response)
        mapper = PageSpeedMapper()

        # Act
        result = mapper.to_core_web_vitals(
            url_id=url_id,
            execution_date=sample_execution_date,
            response=response_dto
        )

        # Assert
        assert isinstance(result, CoreWebVitals)
        assert result.url_id == url_id
        assert result.execution_date == sample_execution_date
        assert result.performance_score == 85.0
        assert result.first_contentful_paint == 1234.5
        assert result.largest_contentful_paint == 2345.6
        assert result.total_blocking_time == 123.4
        assert result.cumulative_layout_shift == 0.05
        assert result.speed_index == 3456.7
        assert result.time_to_first_byte == 234.5
        assert result.time_to_interactive == 4567.8
        assert result.crux_largest_contentful_paint == 2500
        assert result.crux_interaction_to_next_paint == 150
        assert result.crux_cumulative_layout_shift == 0.1
        assert result.crux_first_contentful_paint == 1500
        assert result.crux_time_to_first_byte == 300

    def test_to_core_web_vitals_with_missing_fields(self, sample_execution_date):
        """Test mapper handles missing fields gracefully."""
        # Arrange
        url_id = 456
        minimal_response = {
            "lighthouseResult": {
                "categories": {"performance": {"score": 0.5}},
                "audits": {}
            },
            "loadingExperience": {"metrics": {}}
        }
        response_dto = PageSpeedInsightsResponse(minimal_response)
        mapper = PageSpeedMapper()

        # Act
        result = mapper.to_core_web_vitals(
            url_id=url_id,
            execution_date=sample_execution_date,
            response=response_dto
        )

        # Assert
        assert result.url_id == url_id
        assert result.performance_score == 50.0
        assert result.first_contentful_paint is None
        assert result.crux_largest_contentful_paint is None

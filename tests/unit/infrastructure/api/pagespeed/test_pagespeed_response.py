"""Tests for PageSpeedInsightsResponse DTO."""
import pytest

from src.infrastructure.api.pagespeed.dto.pagespeed_response import (
    PageSpeedInsightsResponse,
)


class TestPageSpeedInsightsResponse:
    """Test suite for PageSpeedInsightsResponse DTO."""

    def test_extract_all_metrics(self, sample_pagespeed_response):
        """Test extracting all metrics from API response."""
        # Act
        dto = PageSpeedInsightsResponse(sample_pagespeed_response)

        # Assert
        assert dto.performance_score == 85.0
        assert dto.first_contentful_paint == 1234.5
        assert dto.largest_contentful_paint == 2345.6
        assert dto.total_blocking_time == 123.4
        assert dto.cumulative_layout_shift == 0.05
        assert dto.speed_index == 3456.7
        assert dto.time_to_first_byte == 234.5
        assert dto.time_to_interactive == 4567.8
        assert dto.crux_largest_contentful_paint == 2500
        assert dto.crux_interaction_to_next_paint == 150
        assert dto.crux_cumulative_layout_shift == 0.1
        assert dto.crux_first_contentful_paint == 1500
        assert dto.crux_time_to_first_byte == 300

    def test_get_all_metrics_dictionary(self, sample_pagespeed_response):
        """Test get_all_metrics returns complete dictionary."""
        # Act
        dto = PageSpeedInsightsResponse(sample_pagespeed_response)
        all_metrics = dto.get_all_metrics()

        # Assert
        assert isinstance(all_metrics, dict)
        assert 'performance_score' in all_metrics
        assert 'first_contentful_paint' in all_metrics
        assert 'crux_largest_contentful_paint' in all_metrics
        assert len(all_metrics) == 13  # 1 score + 7 lab + 5 crux metrics

    def test_missing_performance_score(self):
        """Test handling of missing performance score."""
        # Arrange
        response = {
            "lighthouseResult": {"categories": {}, "audits": {}},
            "loadingExperience": {"metrics": {}}
        }

        # Act
        dto = PageSpeedInsightsResponse(response)

        # Assert
        assert dto.performance_score == 0.0

    def test_missing_lab_metrics(self):
        """Test handling of missing lab metrics."""
        # Arrange
        response = {
            "lighthouseResult": {
                "categories": {"performance": {"score": 0.5}},
                "audits": {}
            },
            "loadingExperience": {"metrics": {}}
        }

        # Act
        dto = PageSpeedInsightsResponse(response)

        # Assert
        assert dto.first_contentful_paint is None
        assert dto.largest_contentful_paint is None
        assert dto.performance_score == 50.0

    def test_missing_crux_metrics(self):
        """Test handling of missing CrUX metrics."""
        # Arrange
        response = {
            "lighthouseResult": {
                "categories": {"performance": {"score": 0.5}},
                "audits": {}
            },
            "loadingExperience": {"metrics": {}}
        }

        # Act
        dto = PageSpeedInsightsResponse(response)

        # Assert
        assert dto.crux_largest_contentful_paint is None
        assert dto.crux_first_contentful_paint is None

    def test_lab_metrics_data_property(self, sample_pagespeed_response):
        """Test lab_metrics_data property returns correct structure."""
        # Act
        dto = PageSpeedInsightsResponse(sample_pagespeed_response)
        lab_data = dto.lab_metrics_data

        # Assert
        assert isinstance(lab_data, dict)
        assert len(lab_data) == 7
        assert 'first_contentful_paint' in lab_data
        assert 'largest_contentful_paint' in lab_data

    def test_field_metrics_data_property(self, sample_pagespeed_response):
        """Test field_metrics_data property returns correct structure."""
        # Act
        dto = PageSpeedInsightsResponse(sample_pagespeed_response)
        field_data = dto.field_metrics_data

        # Assert
        assert isinstance(field_data, dict)
        assert len(field_data) == 5
        assert 'crux_largest_contentful_paint' in field_data
        assert 'crux_first_contentful_paint' in field_data

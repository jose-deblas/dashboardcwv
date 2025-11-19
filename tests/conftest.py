"""Pytest configuration and fixtures."""
import pytest
from datetime import date
from typing import Dict, Any


@pytest.fixture
def sample_pagespeed_response() -> Dict[str, Any]:
    """Sample PageSpeed Insights API response for testing."""
    return {
        "lighthouseResult": {
            "categories": {
                "performance": {
                    "score": 0.85
                }
            },
            "audits": {
                "first-contentful-paint": {"numericValue": 1234.5},
                "largest-contentful-paint": {"numericValue": 2345.6},
                "total-blocking-time": {"numericValue": 123.4},
                "cumulative-layout-shift": {"numericValue": 0.05},
                "speed-index": {"numericValue": 3456.7},
                "server-response-time": {"numericValue": 234.5},
                "interactive": {"numericValue": 4567.8},
            }
        },
        "loadingExperience": {
            "metrics": {
                "LARGEST_CONTENTFUL_PAINT_MS": {"percentile": 2500},
                "INTERACTION_TO_NEXT_PAINT": {"percentile": 150},
                "CUMULATIVE_LAYOUT_SHIFT_SCORE": {"percentile": 0.1},
                "FIRST_CONTENTFUL_PAINT_MS": {"percentile": 1500},
                "EXPERIMENTAL_TIME_TO_FIRST_BYTE": {"percentile": 300},
            }
        }
    }


@pytest.fixture
def sample_execution_date() -> date:
    """Sample execution date for testing."""
    return date(2025, 11, 19)

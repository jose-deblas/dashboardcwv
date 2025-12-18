from datetime import date

import pytest

from src.application.dto.dashboard_dtos import DeviceMetrics


def test_growth_rate_positive_and_delta():
    dm = DeviceMetrics(device="mobile", start_score=50.0, end_score=60.0)
    assert dm.delta == 10.0
    assert pytest.approx(dm.growth_rate, rel=1e-6) == 20.0


def test_growth_rate_negative():
    dm = DeviceMetrics(device="desktop", start_score=80.0, end_score=60.0)
    assert dm.delta == -20.0
    assert pytest.approx(dm.growth_rate, rel=1e-6) == -25.0


def test_growth_rate_with_zero_start_returns_none():
    dm = DeviceMetrics(device="mobile", start_score=0.0, end_score=50.0)
    assert dm.delta == 50.0
    assert dm.growth_rate is None


def test_growth_rate_with_missing_scores_is_none():
    dm1 = DeviceMetrics(device="mobile", start_score=None, end_score=50.0)
    dm2 = DeviceMetrics(device="mobile", start_score=50.0, end_score=None)
    dm3 = DeviceMetrics(device="mobile", start_score=None, end_score=None)

    assert dm1.growth_rate is None
    assert dm2.growth_rate is None
    assert dm3.growth_rate is None

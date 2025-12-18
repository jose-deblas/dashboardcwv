import pytest

from src.dashboard.components.styles import get_growth_color


def test_get_growth_color_positive():
    assert get_growth_color(12.34) == "#16a34a"


def test_get_growth_color_negative():
    assert get_growth_color(-5.0) == "#dc2626"


def test_get_growth_color_zero_or_none():
    assert get_growth_color(0.0) == "#6c757d"
    assert get_growth_color(None) == "#6c757d"

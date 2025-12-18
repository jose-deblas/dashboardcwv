from datetime import date

from src.dashboard.components.chart_renderer import ChartRenderer
from src.application.dto.dashboard_dtos import TimeSeriesPoint


def _count_threshold_shapes(fig):
    shapes = getattr(fig.layout, "shapes", [])
    return [s for s in shapes if getattr(s, "type", None) == "line"]


def test_chart_renderer_adds_threshold_lines_performance():
    renderer = ChartRenderer(red_threshold=40, green_threshold=60)

    data = [
        TimeSeriesPoint(execution_date=date(2025, 1, 1), avg_performance_score=35.0),
        TimeSeriesPoint(execution_date=date(2025, 1, 2), avg_performance_score=70.0),
    ]

    fig = renderer.create_performance_evolution_chart(mobile_data=data, desktop_data=[])

    shapes = _count_threshold_shapes(fig)
    # Expect at least two horizontal line shapes (red and green)
    assert len(shapes) >= 2

    # ensure the threshold y positions exist
    ys = {float(s.y0) for s in shapes}
    assert 40.0 in ys
    assert 60.0 in ys


def test_chart_renderer_adds_threshold_lines_competitor():
    renderer = ChartRenderer(red_threshold=40, green_threshold=60)

    data = [
        TimeSeriesPoint(execution_date=date(2025, 1, 1), avg_performance_score=50.0, brand="A"),
        TimeSeriesPoint(execution_date=date(2025, 1, 2), avg_performance_score=30.0, brand="B"),
    ]

    fig = renderer.create_competitor_evolution_chart(time_series_data=data, device="mobile", target_brands=["A"])

    shapes = _count_threshold_shapes(fig)
    assert len(shapes) >= 2

    ys = {float(s.y0) for s in shapes}
    assert 40.0 in ys
    assert 60.0 in ys

"""Core Web Vitals Entity representing performance metrics."""
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class CoreWebVitals:
    """
    Entity representing Core Web Vitals metrics for a URL.

    Attributes:
        url_id: Reference to the URL being measured
        execution_date: Date when metrics were collected
        performance_score: Overall performance score (0-100)
        first_contentful_paint: FCP metric (ms)
        largest_contentful_paint: LCP metric (ms)
        total_blocking_time: TBT metric (ms)
        cumulative_layout_shift: CLS metric (score)
        speed_index: Speed Index metric (ms)
        time_to_first_byte: TTFB metric (ms)
        time_to_interactive: TTI metric (ms)
        crux_largest_contentful_paint: CrUX LCP (ms)
        crux_interaction_to_next_paint: CrUX INP (ms)
        crux_cumulative_layout_shift: CrUX CLS (score)
        crux_first_contentful_paint: CrUX FCP (ms)
        crux_time_to_first_byte: CrUX TTFB (ms)
    """
    url_id: int
    execution_date: date
    performance_score: Optional[float] = None
    first_contentful_paint: Optional[float] = None
    largest_contentful_paint: Optional[float] = None
    total_blocking_time: Optional[float] = None
    cumulative_layout_shift: Optional[float] = None
    speed_index: Optional[float] = None
    time_to_first_byte: Optional[float] = None
    time_to_interactive: Optional[float] = None
    crux_largest_contentful_paint: Optional[float] = None
    crux_interaction_to_next_paint: Optional[float] = None
    crux_cumulative_layout_shift: Optional[float] = None
    crux_first_contentful_paint: Optional[float] = None
    crux_time_to_first_byte: Optional[float] = None

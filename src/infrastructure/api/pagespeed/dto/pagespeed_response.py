"""Data Transfer Object for PageSpeed Insights API response."""
from typing import Any, Dict, Optional


class PageSpeedInsightsResponse:
    """DTO to extract relevant metrics from PageSpeed Insights API response."""

    def __init__(self, json_data: Dict[str, Any]) -> None:
        """
        Initialize DTO with API response JSON.

        Args:
            json_data: Raw JSON response from PageSpeed Insights API
        """
        self.data = json_data
        self.field_metrics: Dict[str, Any] = self.data.get('loadingExperience', {}).get('metrics', {})
        self.lab_metrics: Dict[str, Any] = self.data.get('lighthouseResult', {}).get('audits', {})
        self.categories: Dict[str, Any] = self.data.get('lighthouseResult', {}).get('categories', {})

    @property
    def performance_score(self) -> float:
        """Get overall performance score (0-100)."""
        score = self.categories.get('performance', {}).get('score')
        return score * 100 if score is not None else 0.0

    @property
    def first_contentful_paint(self) -> Optional[float]:
        """Get First Contentful Paint metric in milliseconds."""
        return self.lab_metrics.get('first-contentful-paint', {}).get('numericValue')

    @property
    def largest_contentful_paint(self) -> Optional[float]:
        """Get Largest Contentful Paint metric in milliseconds."""
        return self.lab_metrics.get('largest-contentful-paint', {}).get('numericValue')

    @property
    def total_blocking_time(self) -> Optional[float]:
        """Get Total Blocking Time metric in milliseconds."""
        return self.lab_metrics.get('total-blocking-time', {}).get('numericValue')

    @property
    def cumulative_layout_shift(self) -> Optional[float]:
        """Get Cumulative Layout Shift metric score."""
        return self.lab_metrics.get('cumulative-layout-shift', {}).get('numericValue')

    @property
    def speed_index(self) -> Optional[float]:
        """Get Speed Index metric in milliseconds."""
        return self.lab_metrics.get('speed-index', {}).get('numericValue')

    @property
    def time_to_first_byte(self) -> Optional[float]:
        """Get Time to First Byte metric in milliseconds."""
        return self.lab_metrics.get('server-response-time', {}).get('numericValue')

    @property
    def time_to_interactive(self) -> Optional[float]:
        """Get Time to Interactive metric in milliseconds."""
        return self.lab_metrics.get('interactive', {}).get('numericValue')

    @property
    def crux_largest_contentful_paint(self) -> Optional[float]:
        """Get CrUX Largest Contentful Paint percentile in milliseconds."""
        return self.field_metrics.get('LARGEST_CONTENTFUL_PAINT_MS', {}).get('percentile')

    @property
    def crux_interaction_to_next_paint(self) -> Optional[float]:
        """Get CrUX Interaction to Next Paint percentile in milliseconds."""
        return self.field_metrics.get('INTERACTION_TO_NEXT_PAINT', {}).get('percentile')

    @property
    def crux_cumulative_layout_shift(self) -> Optional[float]:
        """Get CrUX Cumulative Layout Shift percentile score."""
        return self.field_metrics.get('CUMULATIVE_LAYOUT_SHIFT_SCORE', {}).get('percentile')

    @property
    def crux_first_contentful_paint(self) -> Optional[float]:
        """Get CrUX First Contentful Paint percentile in milliseconds."""
        return self.field_metrics.get('FIRST_CONTENTFUL_PAINT_MS', {}).get('percentile')

    @property
    def crux_time_to_first_byte(self) -> Optional[float]:
        """Get CrUX Time to First Byte percentile in milliseconds."""
        return self.field_metrics.get('EXPERIMENTAL_TIME_TO_FIRST_BYTE', {}).get('percentile')

    @property
    def lab_metrics_data(self) -> Dict[str, Optional[float]]:
        """Get all lab metrics as a dictionary."""
        return {
            'first_contentful_paint': self.first_contentful_paint,
            'largest_contentful_paint': self.largest_contentful_paint,
            'total_blocking_time': self.total_blocking_time,
            'cumulative_layout_shift': self.cumulative_layout_shift,
            'speed_index': self.speed_index,
            'time_to_first_byte': self.time_to_first_byte,
            'time_to_interactive': self.time_to_interactive,
        }

    @property
    def field_metrics_data(self) -> Dict[str, Optional[float]]:
        """Get all CrUX field metrics as a dictionary."""
        return {
            'crux_largest_contentful_paint': self.crux_largest_contentful_paint,
            'crux_interaction_to_next_paint': self.crux_interaction_to_next_paint,
            'crux_cumulative_layout_shift': self.crux_cumulative_layout_shift,
            'crux_first_contentful_paint': self.crux_first_contentful_paint,
            'crux_time_to_first_byte': self.crux_time_to_first_byte,
        }

    def get_all_metrics(self) -> Dict[str, Optional[float]]:
        """
        Get all metrics as a single dictionary.

        Returns:
            Dictionary with all metrics including performance score, lab, and field metrics
        """
        return {
            'performance_score': self.performance_score,
            **self.lab_metrics_data,
            **self.field_metrics_data
        }

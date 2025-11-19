class PageSpeedInsightsMetrics:
    """Class to extract relevant metrics from PageSpeed Insights API response."""
    def __init__(self, json_data):
        self.data = json_data
        self.field_metrics = self.data.get('loadingExperience', {}).get('metrics', {})
        self.lab_metrics = self.data.get('lighthouseResult', {}).get('audits', {})
        self.categories = self.data.get('lighthouseResult', {}).get('categories', {})

    @property
    def performance_score(self):
        score = self.categories.get('performance', {}).get('score', 0)
        return score * 100 if score is not None else 0

    @property
    def first_contentful_paint(self):
        return self.lab_metrics.get('first-contentful-paint', {}).get('numericValue', 0)

    @property
    def largest_contentful_paint(self):
        return self.lab_metrics.get('largest-contentful-paint', {}).get('numericValue', 0)

    @property
    def total_blocking_time(self):
        return self.lab_metrics.get('total-blocking-time', {}).get('numericValue', 0)

    @property
    def cumulative_layout_shift(self):
        return self.lab_metrics.get('cumulative-layout-shift', {}).get('numericValue', 0)

    @property
    def speed_index(self):
        return self.lab_metrics.get('speed-index', {}).get('numericValue', 0)

    @property
    def time_to_first_byte(self):
        return self.lab_metrics.get('server-response-time', {}).get('numericValue', 0)

    @property
    def time_to_interactive(self):
        return self.lab_metrics.get('interactive', {}).get('numericValue', 0)

    @property
    def crux_largest_contentful_paint(self):
        return self.field_metrics.get('LARGEST_CONTENTFUL_PAINT_MS', {}).get('percentile', 0)

    @property
    def crux_interaction_to_next_paint(self):
        return self.field_metrics.get('INTERACTION_TO_NEXT_PAINT', {}).get('percentile', 0)

    @property
    def crux_cumulative_layout_shift(self):
        return self.field_metrics.get('CUMULATIVE_LAYOUT_SHIFT_SCORE', {}).get('percentile', 0)

    @property
    def crux_first_contentful_paint(self):
        return self.field_metrics.get('FIRST_CONTENTFUL_PAINT_MS', {}).get('percentile', 0)

    @property
    def crux_time_to_first_byte(self):
        return self.field_metrics.get('EXPERIMENTAL_TIME_TO_FIRST_BYTE', {}).get('percentile', 0)

    @property
    def lab_metrics_data(self):
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
    def field_metrics_data(self):
        return {
            'crux_largest_contentful_paint': self.crux_largest_contentful_paint,
            'crux_interaction_to_next_paint': self.crux_interaction_to_next_paint,
            'crux_cumulative_layout_shift': self.crux_cumulative_layout_shift,
            'crux_first_contentful_paint': self.crux_first_contentful_paint,
            'crux_time_to_first_byte': self.crux_time_to_first_byte,
        }

    def get_all_metrics(self):
        return {
            'performance_score': self.performance_score,
            **self.lab_metrics_data,
            **self.field_metrics_data
        }

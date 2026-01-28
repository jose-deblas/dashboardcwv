"""
Presenter for transforming performance DTOs into view models.

This presenter contains ALL presentation logic for performance metrics including:
- Delta calculations
- Growth rate calculations
- Color determination
- Value formatting
- Target values

All business logic previously in DeviceMetrics DTO has been moved here.
"""

from typing import List, Optional

from src.application.dto.dashboard_dtos import (
    DeviceMetrics,
    PerformanceMetrics,
    TimeSeriesPoint,
    FilterCriteria,
)
from src.presentation.models.performance_view_model import (
    PerformanceViewModel,
    DeviceMetricsViewModel,
    MetricCardViewModel,
)


class PerformancePresenter:
    """
    Transforms performance DTOs into view models.

    Handles all presentation logic including calculations, formatting,
    and color determination.
    """

    TARGET_MOBILE = 65
    TARGET_DESKTOP = 80

    def present(
        self,
        performance_metrics: PerformanceMetrics,
        mobile_time_series: List[TimeSeriesPoint],
        desktop_time_series: List[TimeSeriesPoint],
    ) -> PerformanceViewModel:
        """
        Transform performance data into view model.

        Args:
            performance_metrics: Performance metrics DTO from use case
            mobile_time_series: Mobile time series data
            desktop_time_series: Desktop time series data

        Returns:
            Complete performance view model ready for rendering
        """
        mobile_vm = self._present_device_metrics(
            performance_metrics.mobile_metrics, "Mobile", self.TARGET_MOBILE
        )

        desktop_vm = self._present_device_metrics(
            performance_metrics.desktop_metrics, "Desktop", self.TARGET_DESKTOP
        )

        active_filters = self._format_active_filters(
            performance_metrics.filter_criteria
        )

        return PerformanceViewModel(
            mobile=mobile_vm,
            desktop=desktop_vm,
            active_filters_display=active_filters,
            has_time_series_data=bool(mobile_time_series or desktop_time_series),
        )

    def _present_device_metrics(
        self, metrics: DeviceMetrics, device_label: str, target: int
    ) -> DeviceMetricsViewModel:
        """
        Transform device metrics with all presentation logic.

        Args:
            metrics: Device metrics DTO
            device_label: Display label ("Mobile" or "Desktop")
            target: Target score for this device

        Returns:
            Device metrics view model with all calculated and formatted values
        """
        has_data = (
            metrics.start_score is not None or metrics.end_score is not None
        )

        # Calculate delta
        delta = None
        if metrics.start_score is not None and metrics.end_score is not None:
            delta = metrics.end_score - metrics.start_score

        # Calculate growth rate
        growth_rate = None
        if (
            delta is not None
            and metrics.start_score
            and metrics.start_score != 0
        ):
            growth_rate = (delta / metrics.start_score) * 100

        # Format cards
        target_card = MetricCardViewModel(
            label="Target",
            value=f"{target}.00",
            delta=None,
            delta_color=None,
            help_text=f"Performance score target for {device_label.lower()}",
        )

        start_card = MetricCardViewModel(
            label="Initial Date",
            value=self._format_score(metrics.start_score),
            delta=None,
        )

        end_card = MetricCardViewModel(
            label="End Date",
            value=self._format_score(metrics.end_score),
            delta=self._format_delta(delta),
            delta_color=self._get_delta_color(delta),
        )

        growth_display = self._format_growth_rate(growth_rate)
        growth_color = self._get_growth_color(growth_rate)

        return DeviceMetricsViewModel(
            device_label=device_label,
            target_card=target_card,
            start_date_card=start_card,
            end_date_card=end_card,
            growth_rate_display=growth_display,
            growth_rate_color=growth_color,
            has_data=has_data,
        )

    def _format_score(self, score: Optional[float]) -> str:
        """
        Format score for display.

        Args:
            score: Score value or None

        Returns:
            Formatted string: "65.00" or "N/A"
        """
        return f"{score:.2f}" if score is not None else "N/A"

    def _format_delta(self, delta: Optional[float]) -> Optional[str]:
        """
        Format delta with sign.

        Args:
            delta: Delta value or None

        Returns:
            Formatted string with sign: "+5.20", "-2.10", or None
        """
        if delta is None:
            return None
        sign = "+" if delta > 0 else ""
        return f"{sign}{delta:.2f}"

    def _format_growth_rate(self, growth_rate: Optional[float]) -> str:
        """
        Format growth rate as percentage.

        Args:
            growth_rate: Growth rate value or None

        Returns:
            Formatted percentage: "+12.34%", "-5.67%", or "N/A"
        """
        if growth_rate is None:
            return "N/A"
        sign = "+" if growth_rate > 0 else ""
        return f"{sign}{growth_rate:.2f}%"

    def _get_delta_color(self, delta: Optional[float]) -> str:
        """
        Determine color based on delta value.

        Args:
            delta: Delta value or None

        Returns:
            Color name: "green", "red", or "neutral"
        """
        if delta is None:
            return "neutral"
        if delta > 0:
            return "green"
        elif delta < 0:
            return "red"
        return "neutral"

    def _get_growth_color(self, growth_rate: Optional[float]) -> str:
        """
        Determine color based on growth rate.

        Args:
            growth_rate: Growth rate value or None

        Returns:
            Color name: "green", "red", or "neutral"
        """
        if growth_rate is None:
            return "neutral"
        if growth_rate > 0:
            return "green"
        elif growth_rate < 0:
            return "red"
        return "neutral"

    def _format_active_filters(self, criteria: FilterCriteria) -> List[str]:
        """
        Format filter criteria for display.

        Args:
            criteria: Filter criteria DTO

        Returns:
            List of formatted filter strings
        """
        filters = []

        # Date range
        filters.append(f"From {criteria.start_date} to {criteria.end_date}")

        # Brands
        if criteria.brands:
            brands = ", ".join(criteria.brands)
        else:
            brands = "All Brands"
        filters.append(f"Brand: {brands}")

        # Countries
        if criteria.countries:
            countries = ", ".join(criteria.countries)
        else:
            countries = "All Countries"
        filters.append(f"Country: {countries}")

        # Page types
        if criteria.page_types:
            page_types = ", ".join(criteria.page_types)
        else:
            page_types = "All Page Types"
        filters.append(f"Page Types: {page_types}")

        return filters

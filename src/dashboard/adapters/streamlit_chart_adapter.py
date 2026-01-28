"""
Streamlit-specific chart rendering adapter.

Converts framework-agnostic ChartViewModel to Plotly figures for Streamlit.
"""

import plotly.graph_objects as go
from typing import Optional

from src.presentation.models.chart_view_model import ChartViewModel
from src.dashboard.components.chart_renderer import ChartRenderer


class StreamlitChartAdapter:
    """
    Adapts ChartViewModel to Plotly figures for Streamlit.

    Uses existing ChartRenderer for threshold rendering while
    converting framework-agnostic chart view models to Plotly.

    Example:
        >>> adapter = StreamlitChartAdapter(red_threshold=40, green_threshold=60)
        >>> chart_vm = ChartViewModel(...)
        >>> fig = adapter.render_chart(chart_vm)
        >>> st.plotly_chart(fig, use_container_width=True)
    """

    def __init__(
        self, red_threshold: float = 40.0, green_threshold: float = 60.0
    ):
        """
        Initialize chart adapter with threshold values.

        Args:
            red_threshold: Lower threshold for performance
            green_threshold: Upper threshold for performance
        """
        self.chart_renderer = ChartRenderer(red_threshold, green_threshold)

    def render_chart(self, chart_vm: ChartViewModel) -> go.Figure:
        """
        Convert ChartViewModel to Plotly Figure.

        Args:
            chart_vm: Framework-agnostic chart view model

        Returns:
            Plotly Figure ready for st.plotly_chart()
        """
        fig = go.Figure()

        # Add traces from view model
        for series in chart_vm.series:
            fig.add_trace(
                go.Scatter(
                    x=[point.date for point in series.data_points],
                    y=[point.value for point in series.data_points],
                    name=series.series_name,
                    line=dict(
                        color=series.color or "blue",
                        width=series.line_width,
                    ),
                    marker=dict(size=series.marker_size),
                    hovertemplate=f"<b>{series.series_name}</b>: %{{y:.2f}}<extra></extra>",
                )
            )

        # Configure layout
        fig.update_layout(
            title=dict(text=chart_vm.title),
            xaxis=dict(showgrid=True),
            yaxis=dict(title=chart_vm.y_axis_label, showgrid=True),
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12),
            ),
            height=chart_vm.height,
        )

        # Add thresholds using existing renderer
        if chart_vm.show_thresholds:
            self.chart_renderer._add_threshold_lines(fig)

        return fig

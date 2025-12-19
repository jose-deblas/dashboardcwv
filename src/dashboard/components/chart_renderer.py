from typing import List, Optional, Dict

import plotly.graph_objects as go

from src.application.dto.dashboard_dtos import TimeSeriesPoint


class ChartRenderer:
    """Simple chart renderer that adds threshold lines to Plotly figures.

    This is intentionally minimal — it only provides the methods used by
    the dashboard and unit tests (adds horizontal threshold lines).
    """

    def __init__(self, red_threshold: float = 40.0, green_threshold: float = 60.0):
        self.red_threshold = float(red_threshold)
        self.green_threshold = float(green_threshold)

    def _add_threshold_lines(self, fig: go.Figure) -> None:
        shapes = list(getattr(fig.layout, "shapes", []) or [])

        # Red threshold line
        shapes.append(
            dict(
                type="line",
                xref="paper",
                x0=0,
                x1=1,
                yref="y",
                y0=self.red_threshold,
                y1=self.red_threshold,
                line=dict(color="#e74c3c", width=2, dash="dash"),
            )
        )

        # Green threshold line
        shapes.append(
            dict(
                type="line",
                xref="paper",
                x0=0,
                x1=1,
                yref="y",
                y0=self.green_threshold,
                y1=self.green_threshold,
                line=dict(color="#2ecc71", width=2, dash="dash"),
            )
        )

        fig.update_layout(shapes=shapes)

    def create_performance_evolution_chart(
        self, mobile_data: List[TimeSeriesPoint], desktop_data: List[TimeSeriesPoint]
    ) -> go.Figure:
        fig = go.Figure()

        # Add simple traces if provided (kept minimal for tests)
        if mobile_data:
            fig.add_trace(
                go.Scatter(
                    x=[p.execution_date for p in mobile_data],
                    y=[p.avg_performance_score for p in mobile_data],
                    name="Mobile",
                    line=dict(color="red", width=3),
                    marker=dict(size=8),
                    hovertemplate="Mobile: %{y:.2f}<extra></extra>",
                )
            )

        if desktop_data:
            fig.add_trace(
                go.Scatter(
                    x=[p.execution_date for p in desktop_data],
                    y=[p.avg_performance_score for p in desktop_data],
                    name="Desktop",
                    line=dict(color="royalblue", width=3),
                    marker=dict(size=8),
                    hovertemplate="Desktop: %{y:.2f}<extra></extra>",
                )
            )
        
        # Layout
        fig.update_layout(
            title=dict(
                text=f" Performance Score Evolution",
            ),
            xaxis=dict(
                showgrid=True,
            ),
            yaxis=dict(
                title="Performance Score",
                showgrid=True,
            ),
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12),
            ),
            height=500,
        )

        self._add_threshold_lines(fig)
        return fig

    def create_competitor_evolution_chart(
        self,
        time_series_data: List[TimeSeriesPoint],
        device: str,
        target_brands: List[str],
        target_brand_colors: Optional[Dict[str, str]] = None,
    ) -> go.Figure:
        fig = go.Figure()

        # Group data by brand
        brands = {}
        for point in time_series_data:
            if point.brand not in brands:
                brands[point.brand] = {"dates": [], "scores": []}
            brands[point.brand]["dates"].append(point.execution_date)
            brands[point.brand]["scores"].append(point.avg_performance_score)

        #take the min and max score to set y axis range
        all_scores = []
        for data in brands.values():
            all_scores.extend(data["scores"])
        if all_scores:
            min_score = min(all_scores) - 1
            max_score = max(all_scores) + 1

        # Build color palette for target brands
        if target_brand_colors is None:
            # Default colors for target brands if not provided
            target_colors = ["red", "royalblue", "purple", "cyan"]
            target_brand_colors = {
                brand: target_colors[i % len(target_colors)]
                for i, brand in enumerate(target_brands)
            }

        # Default colors for non-target brands
        default_colors = ["green", "orange", "skyblue", "pink", "silver"]
        color_idx = 0

        # Add trace for each brand
        for brand, data in brands.items():
            if brand in target_brands:
                color = target_brand_colors.get(brand, "#a7f9ab")
                line_width = 3
                marker_size = 6
            else:
                color = default_colors[color_idx % len(default_colors)]
                color_idx += 1
                line_width = 2
                marker_size = 4

            fig.add_trace(
                go.Scatter(
                    x=data["dates"],
                    y=data["scores"],
                    mode="lines+markers",
                    name=brand,
                    line=dict(color=color, width=line_width),
                    marker=dict(size=marker_size),
                    hovertemplate=f"<b>{brand}</b>: %{{y:.2f}}<extra></extra>",
                )
            )

        # Layout
        fig.update_layout(
            title=dict(
                text=f" {device.capitalize()} Evolution",
            ),
            xaxis=dict(
                showgrid=True,
            ),
            yaxis=dict(
                title="Performance Score",
                showgrid=True,
                range=[min_score, max_score],
            ),
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12),
            ),
            height=500,
        )

        self._add_threshold_lines(fig)
        return fig

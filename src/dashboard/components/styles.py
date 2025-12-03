"""
Dashboard styling and CSS utilities.

This module provides CSS styles for the dashboard, including
traffic light indicators.
"""

def get_weather_give_traffic_light_color(color: str) -> str:
    """
    Return a unicode character representing the traffic light indicator.

    Args:
        color: Traffic light color ('green', 'amber', or 'red')

    Returns:
        Unicode character for sun/cloud/storm
    """
    if color == 'green':
        return '☀️'  # Sun for green
    elif color == 'amber':
        return '⛅'  # Cloudy for amber
    elif color == 'red':
        return '🌩️'  # Storm for red
    else:
        return '❓'  # Unknown


def get_metric_card_html(
    label: str, value: float, delta: float = None, device: str = None
) -> str:
    """
    Generate HTML for metric card.

    Args:
        label: Label for the metric
        value: Metric value
        delta: Optional delta value
        device: Optional device label

    Returns:
        HTML string for metric card
    """
    if delta is not None:
        if delta > 0:
            delta_class = "metric-delta-positive"
            sign = "+"
        elif delta < 0:
            delta_class = "metric-delta-negative"
            sign = ""
        else:
            delta_class = "metric-delta-neutral"
            sign = ""
        delta_html = f'<div class="{delta_class}">{sign}{delta:.2f}</div>'
    else:
        delta_html = ""

    device_html = f'<div style="color: #a7f9ab; font-size: 12px; margin-bottom: 5px;">{device}</div>' if device else ""

    return f"""
    <div class="metric-card">
        {device_html}
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value:.2f}</div>
        {delta_html}
    </div>
    """

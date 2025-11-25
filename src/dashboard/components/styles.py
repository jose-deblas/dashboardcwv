"""
Dashboard styling and CSS utilities.

This module provides CSS styles for the dashboard, including
dark mode support and traffic light indicators.
"""


def get_dark_mode_css() -> str:
    """
    Get CSS for dark mode with custom highlight color.

    Returns:
        CSS string with dark mode styles
    """
    return """
    <style>
    /* Dark mode base styles */
    body, .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }

    /* Streamlit header and toolbar */
    header[data-testid="stHeader"] {
        background-color: #000000 !important;
    }

    /* Streamlit sidebar */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #000000 !important;
    }

    /* Sidebar content */
    .stSidebar .stMarkdown, .stSidebar label {
        color: #ffffff !important;
    }

    /* All text elements default to white */
    p, span, div, label, .stMarkdown {
        color: #ffffff !important;
    }

    a {
        color: red !important;
    }

    /* Headers with highlight color */
    h1, h2, h3, h4, h5, h6 {
        color: #a7f9ab !important;
    }

    /* Dark mode highlight color for important text */
    .highlight {
        color: #a7f9ab !important;
    }

    /* Buttons and interactive elements */
    button, .stButton > button {
        background-color: red !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }

    button:hover, .stButton > button:hover {
        background-color: #8ee092 !important;
        color: #000000 !important;
    }

    /* Any element with #a7f9ab background should have black text */
    [style*="background-color: #a7f9ab"],
    [style*="background: #a7f9ab"] {
        color: #000000 !important;
    }

    /* Header toolbar buttons */
    header[data-testid="stHeader"] button {
        color: #000000 !important;
    }

    /* Checkboxes and form controls */
    .stCheckbox {
        color: #a7f9ab !important;
    }

    input[type="checkbox"] {
        accent-color: #a7f9ab !important;
    }

    /* Select boxes and dropdowns */
    .stSelectbox, select {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #a7f9ab !important;
    }

    /* Text inputs */
    input[type="text"], input[type="number"], textarea {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #a7f9ab !important;
    }

    /* Traffic light indicators */
    .traffic-light-green {
        background-color: #28a745;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }

    .traffic-light-amber {
        background-color: #ffc107;
        color: #000000;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }

    .traffic-light-red {
        background-color: #dc3545;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }

    /* Metric cards */
    .metric-card {
        background-color: #000000;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333333;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }

    .metric-value {
        font-size: 36px;
        font-weight: bold;
        margin: 10px 0;
        color: #ffffff !important;
    }

    .metric-label {
        font-size: 14px;
        color: #a7f9ab !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-delta-positive {
        color: #28a745 !important;
        font-size: 18px;
    }

    .metric-delta-negative {
        color: #dc3545 !important;
        font-size: 18px;
    }

    .metric-delta-neutral {
        color: #ffc107 !important;
        font-size: 18px;
    }

    /* Rankings table */
    .ranking-table {
        width: 100%;
        margin-top: 10px;
    }

    .ranking-row {
        padding: 10px;
        border-bottom: 1px solid #333333;
        color: #ffffff !important;
    }

    .ranking-row.target-brand {
        background-color: #1a1a1a;
        border: 1px solid #a7f9ab;
        font-weight: bold;
    }

    .ranking-position {
        display: inline-block;
        width: 40px;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        color: #a7f9ab !important;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .metric-value {
            font-size: 24px;
        }

        .traffic-light-green,
        .traffic-light-amber,
        .traffic-light-red {
            font-size: 18px;
            padding: 8px 15px;
        }
    }
    </style>
    """


def get_traffic_light_html(color: str, value: float, delta: float = None) -> str:
    """
    Generate HTML for traffic light indicator.

    Args:
        color: Traffic light color ('green', 'amber', or 'red')
        value: Performance score value
        delta: Optional delta value to display

    Returns:
        HTML string for traffic light display
    """
    css_class = f"traffic-light-{color}"

    if delta is not None:
        sign = "+" if delta > 0 else ""
        delta_html = f'<div style="font-size: 18px; margin-top: 5px;">{sign}{delta:.2f}</div>'
    else:
        delta_html = ""

    return f"""
    <div class="{css_class}">
        {value:.2f}
        {delta_html}
    </div>
    """


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

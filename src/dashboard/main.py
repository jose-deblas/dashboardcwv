"""
Core Web Vitals Dashboard - Main Streamlit Application
"""
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Core Web Vitals Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    """Main dashboard application"""

    # Sidebar
    with st.sidebar:
        st.title("📊 CWV Dashboard")
        st.markdown("---")

        # Navigation menu
        page = st.radio(
            "Navigation",
            ["Overview"],
            index=0,
        )

        st.markdown("---")

        # Dark mode toggle placeholder
        dark_mode = st.toggle("🌙 Dark Mode", value=False)

        if dark_mode:
            st.markdown(
                """
                <style>
                :root {
                    --highlight-color: #a7f9ab;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

    # Main content
    st.title("Core Web Vitals Dashboard")
    st.markdown("### Overview")

    st.info(
        "👋 Welcome to the Core Web Vitals Dashboard! "
        "This is a placeholder page. The full implementation is coming soon."
    )

    st.markdown("---")

    # Placeholder for future content
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Performance Score",
            value="--",
            delta="Coming soon",
        )

    with col2:
        st.metric(
            label="Total URLs",
            value="--",
            delta="Coming soon",
        )

    with col3:
        st.metric(
            label="Last Updated",
            value="--",
            delta="Coming soon",
        )

    st.markdown("---")
    st.caption("Core Web Vitals Dashboard v0.1.0")


if __name__ == "__main__":
    main()

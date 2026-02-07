import streamlit as st
import os
from utils.data_loader import load_data
from utils.filters import apply_global_filters

from dashboards.dashboard_overview import show_dashboard
from dashboards.demand_prediction import show_demand_prediction
from dashboards.time_series import show_time_series
from dashboards.pricing_insights import show_pricing_insights

def load_css():
    css_path = os.path.join("assets", "styles.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

# Load data
df = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "📌 Navigation",
    [
        "📊 Dashboard Overview",
        "🤖 Demand Prediction",
        "📈 Time Series Forecasting",
        "💰 Pricing & Revenue Insights"
    ]
)


# Apply global filters
filtered_df = apply_global_filters(df)

st.caption("📊 Observe → 🤖 Predict → 📈 Forecast")

if "Dashboard" in page:
    show_dashboard(filtered_df)
elif "Demand" in page:
    show_demand_prediction(df)
elif "Time Series" in page:
    show_time_series(filtered_df)
else:
    show_pricing_insights(filtered_df)

st.markdown(
    """
    <div class="app-footer">
        © copyrights reserved | 2025 Demand Analytics Project | Built with Streamlit & Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)

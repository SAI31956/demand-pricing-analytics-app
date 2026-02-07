import streamlit as st
import pandas as pd
import plotly.express as px

from utils.ui_components import (
    page_banner,
    animated_counter,
    week_over_week_change,
    no_data_banner
)

# ==================================================
# DASHBOARD OVERVIEW (EDA)
# ==================================================
def show_dashboard(df):

    # --------------------------------------------------
    # Page Header
    # --------------------------------------------------
    page_banner(
        title="Dashboard Overview",
        subtitle="Understand historical demand, pricing, and seasonality",
        emoji="📊"
    )

    # --------------------------------------------------
    # Empty Data Guard
    # --------------------------------------------------
    if df.empty:
        no_data_banner()
        st.warning("No data available to display. Please upload a dataset to see insights.")
        return

    # --------------------------------------------------
    # Base KPI Calculations (SAFE)
    # --------------------------------------------------
    total_revenue = df["revenue"].sum()
    total_units = df["units_sold"].sum()
    avg_price = df["price"].mean()
    avg_discount = df["discount_pct"].mean()
    avg_inventory = df["inventory_level"].mean()

    # --------------------------------------------------
    # KPI Week-over-Week Deltas (INITIALIZE → COMPUTE)
    # --------------------------------------------------
    rev_delta: float | None = None
    unit_delta: float | None = None

    rev_delta = week_over_week_change(df, "revenue")
    unit_delta = week_over_week_change(df, "units_sold")


    # --------------------------------------------------
    # KPI Display (Animated)
    # --------------------------------------------------
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        animated_counter(
            label="Total Revenue",
            value=int(total_revenue) if total_revenue else "N/A",
            icon="💰"
        )
        if rev_delta is not None:
            st.caption(f"📈 {rev_delta:.2f}% vs last week")

    with col2:
        animated_counter(
            label="Total Units Sold",
            value=int(total_units) if total_units else "N/A",
            icon="📦"
        )
        if unit_delta is not None:
            st.caption(f"📈 {unit_delta:.2f}% vs last week")

    with col3:
        animated_counter(
            label="Average Price",
            value=round(avg_price, 2) if not pd.isna(avg_price) else "N/A",
            icon="🏷️"
        )

    with col4:
        animated_counter(
            label="Average Discount %",
            value=round(avg_discount, 2) if not pd.isna(avg_discount) else "N/A",
            icon="📉"
        )

    with col5:
        animated_counter(
            label="Avg Inventory Level",
            value=int(avg_inventory) if not pd.isna(avg_inventory) else "N/A",
            icon="🏭"
        )

    # --------------------------------------------------
    # Time & Trend Analysis
    # --------------------------------------------------
    st.subheader("📈 Time & Trend")

    st.plotly_chart(
        px.line(
            df.sort_values("date"),
            x="date",
            y="units_sold",
            title="Date vs Units Sold"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(
            df.sort_values("date"),
            x="date",
            y="revenue",
            title="Date vs Revenue"
        ),
        use_container_width=True
    )

    # --------------------------------------------------
    # Seasonality & Weekly Patterns
    # --------------------------------------------------
    st.subheader("📆 Seasonality & Weekly Patterns")

    st.plotly_chart(
        px.bar(
            df.groupby("season", as_index=False)["units_sold"].mean(),
            x="season",
            y="units_sold",
            title="Season vs Average Units Sold"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.bar(
            df.groupby("day_of_week", as_index=False)["units_sold"].mean(),
            x="day_of_week",
            y="units_sold",
            title="Day of Week vs Average Units Sold"
        ),
        use_container_width=True
    )

    heatmap_df = df.pivot_table(
        index="day_of_week",
        columns="season",
        values="units_sold",
        aggfunc="mean"
    )

    st.plotly_chart(
        px.imshow(
            heatmap_df,
            title="Day of Week × Season Heatmap",
            aspect="auto"
        ),
        use_container_width=True
    )

    # --------------------------------------------------
    # Product & Pricing Insights
    # --------------------------------------------------
    st.subheader("🛒 Product & Pricing Insights")

    st.plotly_chart(
        px.bar(
            df.groupby("category", as_index=False)["units_sold"].sum(),
            x="category",
            y="units_sold",
            title="Category vs Units Sold"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.scatter(
            df,
            x="price",
            y="units_sold",
            title="Price vs Units Sold"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.scatter(
            df,
            x="price",
            y="competitor_price",
            title="Price vs Competitor Price"
        ),
        use_container_width=True
    )
        # --------------------------------------------------
    # Feature Correlation Analysis
    # --------------------------------------------------
    st.subheader("🔗 Feature Correlation Analysis")

    numeric_cols = [
        "price",
        "cost",
        "discount_pct",
        "units_sold",
        "revenue",
        "inventory_level",
        "competitor_price",
        "profit",
        "margin_pct",
        "price_diff_competitor"
    ]

    # Keep only columns that actually exist
    numeric_cols = [col for col in numeric_cols if col in df.columns]

    corr_df = df[numeric_cols].corr()

    st.plotly_chart(
        px.imshow(
            corr_df,
            text_auto=".2f",
            color_continuous_scale="RdBu",
            title="Feature Correlation Heatmap",
            aspect="auto"
        ),
        use_container_width=True
    )

    st.info(
        "📌 Correlation insights help identify key demand drivers, multicollinearity "
        "between pricing variables, and relationships between revenue, profit, and units sold."
    )


    # --------------------------------------------------
    # Interpretation
    # --------------------------------------------------
    st.info(
        "📌 Key Insight: Demand shows strong seasonality and weekday effects. "
        "Pricing and discounts significantly influence sales volume, while inventory "
        "levels can constrain realized demand."
    )

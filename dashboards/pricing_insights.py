import streamlit as st
import plotly.express as px

def show_pricing_insights(df):

    st.title("💰 Pricing & Revenue Insights")

    if df.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
        st.stop()

    st.plotly_chart(
        px.scatter(
            df,
            x="price",
            y="units_sold",
            color="season",
            title="Price vs Units Sold (by Season)"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.scatter(
            df,
            x="discount_pct",
            y="units_sold",
            color="day_of_week",
            title="Discount % vs Units Sold (by Day of Week)"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(
            df,
            x="date",
            y="revenue",
            color="season",
            title="Revenue Over Time (Season-wise)"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.scatter(
            df,
            x="inventory_level",
            y="units_sold",
            title="Inventory Level vs Units Sold"
        ),
        use_container_width=True
    )

    st.info(
        "Insights: Demand is price-sensitive, discounts work best on specific weekdays, "
        "and low inventory can cap realized sales."
    )

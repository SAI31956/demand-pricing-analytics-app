import streamlit as st
import pandas as pd

def apply_global_filters(df):

    st.sidebar.title("Global Filters")

    # Reset button
    if st.sidebar.button("🔄 Reset Filters"):
        for key in list(st.session_state.keys()):
            if key.startswith("filter_"):
                del st.session_state[key]
        st.rerun()

    categories = st.sidebar.multiselect(
        "Product Category",
        df["category"].unique(),
        default=df["category"].unique(),
        key="filter_category"
    )

    products = st.sidebar.multiselect(
        "Product ID (Optional)",
        df["product_id"].unique(),
        key="filter_product"
    )

    seasons = st.sidebar.multiselect(
        "Season",
        df["season"].unique(),
        default=df["season"].unique(),
        key="filter_season"
    )

    days = st.sidebar.multiselect(
        "Day of Week",
        df["day_of_week"].unique(),
        default=df["day_of_week"].unique(),
        key="filter_day"
    )

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    start_date, end_date = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        key="filter_date"
    )

    filtered_df = df[
        (df["category"].isin(categories)) &
        (df["season"].isin(seasons)) &
        (df["day_of_week"].isin(days)) &
        (df["date"].between(
            pd.to_datetime(start_date),
            pd.to_datetime(end_date)
        ))
    ]

    if products:
        filtered_df = filtered_df[filtered_df["product_id"].isin(products)]

    return filtered_df

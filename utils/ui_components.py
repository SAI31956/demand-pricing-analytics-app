import streamlit as st
import pandas as pd
import time

# --------------------------------------------------
# Page Banner
# --------------------------------------------------
def page_banner(title, subtitle, emoji=""):
    st.markdown(
        f"""
        <div class="app-header">
            <h1>{emoji} {title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Animated KPI Counter
# --------------------------------------------------
def animated_counter(label, value, icon="", duration=1.2):
    placeholder = st.empty()

    if value in ["N/A", None] or pd.isna(value):
        placeholder.metric(label, "N/A")
        return

    steps = 25
    sleep_time = duration / steps

    for i in range(1, steps + 1):
        current = value * i / steps
        placeholder.metric(
            f"{icon} {label}",
            f"{current:,.0f}" if isinstance(value, (int, float)) else current
        )
        time.sleep(sleep_time)


# --------------------------------------------------
# KPI Card (Static – for non-animated use)
# --------------------------------------------------
def kpi_card(icon, label, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-value">{value}</div>
            <div>{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Week-over-Week KPI Change
# --------------------------------------------------
def week_over_week_change(df, column):
    if df.empty:
        return None

    df = df.sort_values("date")

    latest = df[df["date"] >= df["date"].max() - pd.Timedelta(days=7)]
    previous = df[
        (df["date"] < df["date"].max() - pd.Timedelta(days=7)) &
        (df["date"] >= df["date"].max() - pd.Timedelta(days=14))
    ]

    if latest.empty or previous.empty:
        return None

    curr = latest[column].sum()
    prev = previous[column].sum()

    if prev == 0:
        return None

    return ((curr - prev) / prev) * 100


# --------------------------------------------------
# No Data Banner
# --------------------------------------------------
def no_data_banner():
    st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")

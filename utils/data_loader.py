import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(
        base_dir, "data", "processed", "ecommerce_pricing_clean.csv"
    )

    df = pd.read_csv(data_path)

    df["date"] = pd.to_datetime(
        df["date"],
        dayfirst=True,
        errors="coerce"
    )

    # Drop rows where date could not be parsed
    df = df.dropna(subset=["date"])

    return df

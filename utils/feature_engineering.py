import streamlit as st
import joblib
import os
import pandas as pd

# --------------------------------------------------
# Cache decorator fallback (VERY IMPORTANT)
# --------------------------------------------------
cache_decorator = (
    st.cache_data if hasattr(st, "cache_data")
    else st.cache_resource if hasattr(st, "cache_resource")
    else st.cache
)

# --------------------------------------------------
# Feature Encoding
# --------------------------------------------------
def encode_features(df):
    return pd.get_dummies(
        df,
        columns=["season", "day_of_week"],
        drop_first=True
    )

# --------------------------------------------------
# Load Saved Demand Model
# --------------------------------------------------
@cache_decorator
def load_demand_model():
    model_path = os.path.join("models", "demand_model.pkl")
    return joblib.load(model_path)

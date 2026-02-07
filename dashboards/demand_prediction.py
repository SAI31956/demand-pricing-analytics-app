import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from utils.feature_engineering import encode_features, load_demand_model

def show_demand_prediction(df):

    st.title("🤖 Demand Prediction")

    if df.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
        st.stop()

    st.subheader("🤖 AI-Powered Demand Prediction")
    st.caption("Simulate demand based on pricing, competition, and seasonality")

    model_df = encode_features(df)

    X = model_df.drop(
        ["units_sold", "date", "product_id", "category", "revenue"],
        axis=1
    )
    y = model_df["units_sold"]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )
    model.fit(X, y)

    st.subheader("Simulation Inputs")

    price = st.number_input("Price", value=float(df["price"].mean()))
    discount = st.number_input("Discount %", value=float(df["discount_pct"].mean()))
    competitor_price = st.number_input("Competitor Price", value=float(df["competitor_price"].mean()))
    inventory = st.number_input("Inventory Level", value=int(df["inventory_level"].mean()))
    cost = st.number_input("Cost", value=float(df["cost"].mean()))

    season = st.selectbox("Season", df["season"].unique())
    day = st.selectbox("Day of Week", df["day_of_week"].unique())

    input_data = {col: 0 for col in X.columns}
    input_data.update({
        "price": price,
        "discount_pct": discount,
        "competitor_price": competitor_price,
        "inventory_level": inventory,
        "cost": cost
    })

    if f"season_{season}" in input_data:
        input_data[f"season_{season}"] = 1

    if f"day_of_week_{day}" in input_data:
        input_data[f"day_of_week_{day}"] = 1

    input_df = pd.DataFrame([input_data])

    predicted_units = model.predict(input_df)[0]
    revenue = price * predicted_units
    profit = (price - cost) * predicted_units

    st.metric("Predicted Units Sold", round(predicted_units))
    st.metric("Expected Revenue", round(revenue, 2))
    st.metric("Expected Profit", round(profit, 2))
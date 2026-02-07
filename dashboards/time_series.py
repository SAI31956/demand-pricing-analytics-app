from pyexpat import model
import joblib
import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import os

model_path = os.path.join("models", "arima_model.pkl")

def show_time_series(df):

    st.title("📈 Time Series Forecasting")

    if df.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
        st.stop()

    daily_demand = (
        df.groupby("date")["units_sold"]
        .sum()
        .sort_index()
    )

    st.subheader("Trend & Seasonality")

    decomposition = seasonal_decompose(
        daily_demand,
        model="additive",
        period=7
    )

    st.line_chart(decomposition.trend)
    st.line_chart(decomposition.seasonal)

    model = ARIMA(daily_demand, order=(1,1,1))
    model_fit = model.fit()
    
    joblib.dump(model_fit, "models/arima_model.pkl")

    forecast = model_fit.forecast(30)

    forecast_df = pd.DataFrame({
        "date": pd.date_range(
            daily_demand.index.max(),
            periods=30,
            freq="D"
        ),
        "units_sold": forecast,
        "type": "Forecast"
    })

    hist_df = daily_demand.reset_index()
    hist_df["type"] = "Historical"

    combined = pd.concat([hist_df, forecast_df])

    st.plotly_chart(
        px.line(
            combined,
            x="date",
            y="units_sold",
            color="type",
            title="Historical Demand with 30-Day Forecast"
        ),
        use_container_width=True
    )

    st.info("The forecast captures weekly seasonality and overall demand trend.")

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Move up one level to access project_folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import API wrapper
from project_folder.api_wrapper import PySimFin  # Directly import PySimFin without "project_folder"

# Set up the page
st.title("📊 Live Trading Dashboard")

# Initialize API wrapper
api = PySimFin()

# Stock selection
st.sidebar.subheader("Select a Stock")
ticker = st.sidebar.selectbox("Choose a ticker:", ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "META"])

# Date range selection
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-03-01"))

# Fetch stock data
if st.sidebar.button("Fetch Stock Data"):
    with st.spinner("Fetching stock data..."):
        df_prices = api.get_share_prices(ticker, start_date.strftime("%Y-%m-%d"))
        
        if df_prices.empty:
            st.error("No data found for the selected date range.")
        else:
            st.success(f"Showing stock data for {ticker}")
            st.write(df_prices.head())  # Show data preview

            # Plot stock prices
            fig = px.line(df_prices, x=df_prices.index, y="Last Closing Price", title=f"{ticker} Stock Prices")
            st.plotly_chart(fig)

# Placeholder for ML model (to be implemented)
st.sidebar.subheader("Run ML Model")
if st.sidebar.button("Predict Stock Movement"):
    st.warning("ML model integration coming soon!")
# Backtesting Page
import streamlit as st
import pandas as pd

st.title("📉 Backtesting Strategy")

st.markdown("""
Backtesting simulates how a trading strategy based on ML predictions would have performed historically.

We assume:
- Buy if tomorrow's **Predicted Close** > today's **Close**
- Sell otherwise (or hold cash)
- No leverage, fees, or slippage

Let's see how it would have done!
""")

# Load prediction data
file_path_ml = "data/ml_predictions.csv"
@st.cache_data
def load_predictions():
    return pd.read_csv(file_path_ml, parse_dates=["Date"])

df_preds = load_predictions()

# Sidebar for ticker selection
ticker = st.sidebar.selectbox("Choose a ticker:", df_preds["Ticker"].unique())
df_ticker = df_preds[df_preds["Ticker"] == ticker].sort_values("Date").copy()

# Create trading signal: Buy if predicted_close > today's close
df_ticker["Signal"] = (df_ticker["Predicted_Close"] > df_ticker["Close"]).astype(int)

# Strategy returns (assume next day's return if signal was 1)
df_ticker["Return"] = df_ticker["Close"].pct_change()
df_ticker["Strategy_Return"] = df_ticker["Signal"].shift(1) * df_ticker["Return"]

# Cumulative performance
df_ticker["Cumulative_Market"] = (1 + df_ticker["Return"]).cumprod()
df_ticker["Cumulative_Strategy"] = (1 + df_ticker["Strategy_Return"]).cumprod()

# Plot
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Cumulative_Market"], name="Market Return", line=dict(color="gray")))
fig.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Cumulative_Strategy"], name="Strategy Return", line=dict(color="orange")))
fig.update_layout(title=f"{ticker} Strategy vs Market", xaxis_title="Date", yaxis_title="Cumulative Return", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Show metrics
st.metric("Strategy Final Return", f"{df_ticker['Cumulative_Strategy'].iloc[-1]:.2f}x")
st.metric("Market Final Return", f"{df_ticker['Cumulative_Market'].iloc[-1]:.2f}x")

st.markdown("## 🧠 XGBoost Regressor Model Overview")

st.markdown(
    """
    The **XGBoost Regressor** is a gradient-boosted decision tree model we used to predict the 
    **next-day closing price** of each BigTech stock.

    ---
    ### 🔍 Why XGBoost?
    - **Handles complex patterns** in financial time series
    - **Regularized** to reduce overfitting
    - **Fast and scalable**, especially for structured data
    - Outperforms traditional regression models on many tabular tasks

    ---
    ### 📊 Model Inputs
    The model uses only **price-based features**:
    - Open, Close, and Volume
    - Lagged Close prices (e.g., previous day’s Close)

    ---
    ### 📈 Performance Summary (per stock)
    Below are the model performance metrics on the test data:
    """
)

# Create a table using st.table or st.dataframe
import pandas as pd

metrics = pd.DataFrame({
    "Company": ["AAPL", "GOOG", "MSFT", "META", "NVDA", "AMZN"],
    "R² Score": [-0.1416, 0.9749, 0.1757, 0.7487, -1.0855, 0.9963],
    "RMSE": [10.98, 2.05, 34.21, 36.41, 19.62, 1.24],
    "MAE": [8.76, 1.66, 22.43, 15.07, 15.11, 0.87]
})

st.dataframe(metrics.style.format({"R² Score": "{:.4f}", "RMSE": "{:.2f}", "MAE": "{:.2f}"}))

st.markdown(
    """
    🟢 **High accuracy** was observed for Amazon (AMZN) and Google (GOOG), with R² scores close to 1. But we have to bear in mind that the model is very likely overfitting for these two stocks, the R² scores are too high for stock prices.

    🔴 **Poor performance** on Nvidia (NVDA) and Apple (AAPL), indicating the model struggled to generalize well.

    > These differences may reflect the volatility or noise in each stock’s price patterns. Future improvements 
    could include feature engineering (e.g., moving averages) or adding financial indicators.

    ---
    """
)
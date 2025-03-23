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
file_path_ml = "/Users/robertkoegel/Python_for_Data_Analysis_II/Group_project/ml_predictions.csv"
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
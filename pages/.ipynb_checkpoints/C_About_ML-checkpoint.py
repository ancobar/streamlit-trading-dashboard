import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load processed data
file_path = "data/processed_data_enhanced.csv"
df = pd.read_csv(file_path, parse_dates=["Date"])

# Page title
st.title("📘 About the Machine Learning Model")

# Feature Engineering Overview
st.header("Feature Engineering Overview")
st.write("""
We used various technical indicators and stock price features to train our Machine Learning model:
- **Price Changes**: 1-day, 3-day, and 7-day percentage changes
- **Moving Averages**: 7-day, 14-day, and 20-day moving averages
- **Volatility**: Standard deviation over 7 days
- **Relative Strength Index (RSI)**: 14-day RSI indicator
- **Bollinger Bands**: 20-day upper and lower bands
- **Exponential Moving Averages (EMA)**: 12-day and 26-day EMAs
- **MACD Indicator**: Difference between 12-day and 26-day EMAs
""")

# ML Performance Overview
st.header("🤖 Machine Learning Model Performance")
st.write("We trained different classification models to predict stock price movements:")
st.write("""
- **Logistic Regression**: A baseline linear model that assumes a linear relationship between features.
- **Random Forest Classifier**: An ensemble model that improves accuracy by training multiple decision trees.
- **XGBoost Classifier**: A gradient boosting model optimized for tabular data, handling complex patterns better.
""")

# Model Performance Table
performance_data = {
    "Model": ["Logistic Regression", "Random Forest", "XGBoost"],
    "Accuracy": [0.55, 0.53, 0.51],
    "Precision": [0.54, 0.52, 0.52],
    "Recall": [0.55, 0.53, 0.51],
    "F1-score": [0.48, 0.51, 0.51]
}
performance_df = pd.DataFrame(performance_data)
st.table(performance_df)

# Portfolio Simulation Explanation
st.header("📈 Portfolio Simulation Overview")
st.write("""
To evaluate the trading strategy, we implemented a **Buy-Hold-Sell** simulation based on model predictions.

**Trading Strategy Assumptions:**
- Initial capital: **$10,000**, equally distributed among the six BigTech stocks.
- **Buy** if there is enough capital. The minimum capital available has to be 500 at all times.
- **Sell** if price **drops by more than 5%** (stop-loss) or **rises by more than 10%** (profit-taking).

**Simulation Execution:**
- Iterate through historical stock prices day by day.
- Use ML model predictions to determine whether to Buy, Hold, or Sell.
- Update **capital, stock holdings, and portfolio value** over time.
""")

# 📊 Portfolio Performance Over Time
st.header("📈 Portfolio Performance Over Time")

# Process portfolio data
df_plot = df.groupby("Date")["Total Portfolio Value"].last().reset_index()
df_plot["Portfolio Value Smoothed"] = df_plot["Total Portfolio Value"].rolling(window=7).mean()

# Ensure Date column is in datetime format
df_plot["Date"] = pd.to_datetime(df_plot["Date"])

# Create figure and axis for the plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_plot["Date"], df_plot["Portfolio Value Smoothed"], label="Total Portfolio Value", color="blue")

# Format x-axis for better readability
ax.set_xlabel("Date")
ax.set_ylabel("Portfolio Value ($)")
ax.set_title("📈 Portfolio Performance Over Time")
ax.xaxis.set_major_locator(mdates.YearLocator(1))  # Show labels every year
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))  # Format as Year-Month
ax.tick_params(axis="x", rotation=45)  # Rotate x-axis labels

# Add legend and grid
ax.legend()
ax.grid(True, linestyle="--", alpha=0.7)

# Display the plot in Streamlit
st.pyplot(fig)
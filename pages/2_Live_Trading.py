import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Define file path for processed data
file_path = "/Users/robertkoegel/Python_for_Data_Analysis_II/Group_project/data/processed_data.csv"
file_path_ml = "/Users/robertkoegel/Python_for_Data_Analysis_II/Group_project/data/ml_predictions.csv"
# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(file_path, parse_dates=["Date"])
    return df
df = load_data()

@st.cache_data
def load_predictions():
    return pd.read_csv(file_path_ml, parse_dates=["Date"])
df_preds = load_predictions()

# Set up Streamlit page
st.title("📈 Live Trading Dashboard")

# Stock selection
st.sidebar.subheader("Select a Stock")
ticker = st.sidebar.selectbox("Choose a ticker:", df["Ticker"].unique())

# Date range selection
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-03-01"))

# Filter data based on user selection
df_filtered = df[(df["Ticker"] == ticker) & 
                 (df["Date"] >= pd.to_datetime(start_date)) & 
                 (df["Date"] <= pd.to_datetime(end_date))]

# Filter ML predictions
df_preds_filtered = df_preds[
    (df_preds["Ticker"] == ticker) &
    (df_preds["Date"] >= pd.to_datetime(start_date)) &
    (df_preds["Date"] <= pd.to_datetime(end_date))
].dropna(subset=["Predicted_Close"])

# Display if data exists
if not df_filtered.empty:
    st.success(f"Showing stock data for {ticker}")

    # Summary Statistics (Close only)
    st.subheader("📊 Summary Statistics")
    summary_stats = df_filtered["Close"].describe().drop(["count"]).to_frame().T
    styled_stats = summary_stats.style \
        .format("{:.2f}") \
        .set_properties(**{
            'text-align': 'center',
            'font-size': '18px'
        }) \
        .set_table_styles([
            {'selector': 'th', 'props': [('font-size', '18px'), ('text-align', 'center')]},
            {'selector': 'td', 'props': [('font-size', '18px'), ('text-align', 'center')]}
        ]) \
        .background_gradient(cmap="Blues")
    st.dataframe(styled_stats, use_container_width=True)
    
    # Import lightweight chart component
    from streamlit_lightweight_charts import renderLightweightCharts

    # Format data for the price and volume chart
    price_data = [
        {
            "time": row["Date"].strftime("%Y-%m-%d"),
            "value": row["Close"]
        }
        for _, row in df_filtered.iterrows()
    ]

    volume_data = [
        {
            "time": row["Date"].strftime("%Y-%m-%d"),
            "value": row["Volume"]
        }
        for _, row in df_filtered.iterrows()
    ]

    # Chart options
    chart_options = {
        "height": 600,
        "rightPriceScale": {
            "scaleMargins": {
                "top": 0.2,
                "bottom": 0.25,
            },
            "borderVisible": False,
        },
        "layout": {
            "background": {
                "type": 'solid',
                "color": '#ffffff'
            },
            "textColor": '#222',
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(200, 200, 200, 0.3)',
            },
            "horzLines": {
                "color": 'rgba(200, 200, 200, 0.6)',
            }
        },
        "timeScale": {
        "timeVisible": True,
        "secondsVisible": False,
        "borderVisible": True,
        "barSpacing": 15
        },
        "legend": {
        "visible": True,
        "position": "top"
        }
    }

    # Series for price + volume
    series = [
        {
            "type": 'Area',
            "data": price_data,
            "options": {
                "topColor": 'rgba(38,198,218, 0.56)',
                "bottomColor": 'rgba(38,198,218, 0.04)',
                "lineColor": 'rgba(38,198,218, 1)',
                "lineWidth": 2,
            }
        },
        {
            "type": 'Histogram',
            "data": volume_data,
            "options": {
                "color": '#26a69a',
                "priceFormat": {"type": 'volume'},
                "priceScaleId": "",
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0.7,
                    "bottom": 0,
                }
            }
        }
    ]

    # Render chart
    st.subheader("📈 Price and Volume Chart")
    renderLightweightCharts([{"chart": chart_options, "series": series}], 'priceAndVolume')

else:
    st.error("No data found for the selected date range.")

# 📈 ML Prediction Chart
if not df_preds_filtered.empty:
    st.subheader("🧠 ML Predicted vs Actual Closing Price")

    fig = go.Figure()

    # Actual
    fig.add_trace(go.Scatter(
        x=df_preds_filtered["Date"],
        y=df_preds_filtered["Close"],
        mode="lines",
        name="Actual Close",
        line=dict(color="blue")
    ))

    # Predicted
    fig.add_trace(go.Scatter(
        x=df_preds_filtered["Date"],
        y=df_preds_filtered["Predicted_Close"],
        mode="lines",
        name="Predicted Close",
        line=dict(color="orange")
    ))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No ML predictions available for this selection.")
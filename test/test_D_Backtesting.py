import pytest
import pandas as pd
from pages import D_Backtesting as bt

# --------------------------------
# Test: load_predictions()
# --------------------------------
def test_load_predictions_returns_dataframe():
    df = bt.load_predictions()
    assert isinstance(df, pd.DataFrame)

def test_load_predictions_expected_columns():
    df = bt.load_predictions()
    for col in ["Date", "Ticker", "Predicted_Close", "Close"]:
        assert col in df.columns

# --------------------------------
# Test: signal generation and return logic
# --------------------------------
def test_strategy_signal_logic():
    df = bt.load_predictions()
    ticker = df["Ticker"].unique()[0]
    df_ticker = df[df["Ticker"] == ticker].copy()
    df_ticker["Signal"] = (df_ticker["Predicted_Close"] > df_ticker["Close"]).astype(int)
    
    assert df_ticker["Signal"].isin([0, 1]).all()

def test_strategy_return_shape_matches_signal():
    df = bt.load_predictions()
    ticker = df["Ticker"].unique()[0]
    df_ticker = df[df["Ticker"] == ticker].copy()
    df_ticker["Signal"] = (df_ticker["Predicted_Close"] > df_ticker["Close"]).astype(int)
    df_ticker["Return"] = df_ticker["Close"].pct_change()
    df_ticker["Strategy_Return"] = df_ticker["Signal"].shift(1) * df_ticker["Return"]

    assert len(df_ticker["Return"]) == len(df_ticker["Strategy_Return"])

def test_cumulative_returns_not_empty():
    df = bt.load_predictions()
    ticker = df["Ticker"].unique()[0]
    df_ticker = df[df["Ticker"] == ticker].copy()
    df_ticker["Signal"] = (df_ticker["Predicted_Close"] > df_ticker["Close"]).astype(int)
    df_ticker["Return"] = df_ticker["Close"].pct_change()
    df_ticker["Strategy_Return"] = df_ticker["Signal"].shift(1) * df_ticker["Return"]
    df_ticker["Cumulative_Strategy"] = (1 + df_ticker["Strategy_Return"]).cumprod()
    df_ticker["Cumulative_Market"] = (1 + df_ticker["Return"]).cumprod()

    assert not df_ticker["Cumulative_Strategy"].isna().all()
    assert not df_ticker["Cumulative_Market"].isna().all()
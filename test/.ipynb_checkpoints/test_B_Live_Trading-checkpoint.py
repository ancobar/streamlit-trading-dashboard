import pytest
import pandas as pd
import pages.B_Live_Trading as lt

# ---------------------------
# Test: load_data
# ---------------------------
def test_load_data_returns_dataframe():
    df = lt.load_data()
    assert isinstance(df, pd.DataFrame)


def test_load_data_has_expected_columns():
    df = lt.load_data()
    assert "Date" in df.columns
    assert "Ticker" in df.columns
    assert "Close" in df.columns


# ---------------------------
# Test: load_predictions
# ---------------------------
def test_load_predictions_returns_dataframe():
    df_preds = lt.load_predictions()
    assert isinstance(df_preds, pd.DataFrame)


def test_load_predictions_has_expected_columns():
    df_preds = lt.load_predictions()
    assert "Date" in df_preds.columns
    assert "Predicted_Close" in df_preds.columns


# ---------------------------
# Test: filtering logic
# ---------------------------
def test_filtering_logic():
    df = lt.load_data()
    ticker = df["Ticker"].unique()[0]
    start_date = pd.to_datetime("2024-01-01")
    end_date = pd.to_datetime("2024-03-01")
    df_filtered = df[(df["Ticker"] == ticker) & 
                     (df["Date"] >= start_date) & 
                     (df["Date"] <= end_date)]

    assert all(df_filtered["Ticker"] == ticker)
    assert df_filtered["Date"].min() >= start_date
    assert df_filtered["Date"].max() <= end_date

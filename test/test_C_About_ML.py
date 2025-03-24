import pytest
import pandas as pd
from pages import C_About_ML as about

# Test that data loads correctly and is a DataFrame
def test_data_loads_as_dataframe():
    assert isinstance(about.df, pd.DataFrame)

# Test expected columns in loaded data
def test_data_has_expected_columns():
    expected_cols = ["Date", "Total Portfolio Value"]
    for col in expected_cols:
        assert col in about.df.columns

# Test portfolio value smoothing logic
def test_portfolio_smoothing_column_exists():
    df_plot = about.df.groupby("Date")["Total Portfolio Value"].last().reset_index()
    df_plot["Portfolio Value Smoothed"] = df_plot["Total Portfolio Value"].rolling(window=7).mean()
    assert "Portfolio Value Smoothed" in df_plot.columns
    assert not df_plot["Portfolio Value Smoothed"].isnull().all()

# Test date conversion logic
def test_date_column_is_datetime():
    df_plot = about.df.groupby("Date")["Total Portfolio Value"].last().reset_index()
    df_plot["Date"] = pd.to_datetime(df_plot["Date"])
    assert pd.api.types.is_datetime64_any_dtype(df_plot["Date"])

# Optional: Test performance_data is a valid structure
def test_model_performance_data_structure():
    assert isinstance(about.performance_data, dict)
    assert "Model" in about.performance_data
    assert len(about.performance_data["Model"]) == 3
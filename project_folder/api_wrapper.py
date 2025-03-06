import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load API key from environment file
dotenv_path = "/Users/robertkoegel/Python_for_Data_Analysis_II/Group_project/project_folder/API_KEY.env"
load_dotenv(dotenv_path)

SIMFIN_API_KEY = os.getenv("SIMFIN_API_KEY")
print("Loaded API Key:", SIMFIN_API_KEY)

class PySimFin:
    def __init__(self):
        """Initialize the API wrapper with the base URL and headers."""
        self.base_url = "https://backend.simfin.com/api/v3"
        self.headers = {"accept": "application/json", "api-key": SIMFIN_API_KEY}

    def get_share_prices(self, ticker: str, start: str):
        """Fetch share prices for a given ticker from a specific start date."""
        url = f"{self.base_url}/companies/prices"
        params = {"ticker": ticker, "start": start}
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
                columns = data.get("columns", [])
                price_data = data.get("data", [])
                df = pd.DataFrame(price_data, columns=columns)
                df["date"] = pd.to_datetime(df["Date"])
                df.set_index("date", inplace=True)
                return df
        return pd.DataFrame()

    def get_financial_statement(self, ticker: str, statements: str, period: str):
        """Fetch financial statements (income, balance sheet, cash flow) for a given ticker."""
        url = f"{self.base_url}/companies/statements/compact"
        params = {"ticker": ticker, "statements": statements, "period": period}
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
                statements_list = data.get("statements", [])
                if statements_list:
                    statement_data = statements_list[0]
                    columns = statement_data.get("columns", [])
                    financial_data = statement_data.get("data", [])
                    df = pd.DataFrame(financial_data, columns=columns)
                    return df
        return pd.DataFrame()

# Example usage (for testing purposes)
if __name__ == "__main__":
    api = PySimFin()
    df_prices = api.get_share_prices("AAPL", "2023-01-01")
    print(df_prices.head())

    df_income_statement = api.get_financial_statement("AAPL", "pl", "fy")
    print(df_income_statement.head())
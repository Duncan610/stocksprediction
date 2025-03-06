# src/stockml/data_ingestion.py
import os
import requests
from typing import Dict
import pandas as pd
from src.utils.logger import logger
from src.utils.exception import DataIngestionError
from src.config.config import DATA_DIR, ALPHA_VANTAGE_URL

class DataIngestion:
    def __init__(self, api_key: str, symbol: str, output_dir: str = DATA_DIR):
        self.api_key = api_key  # API Key passed from ingest_stock_data.py
        self.symbol = symbol
        self.url = ALPHA_VANTAGE_URL
        self.output_dir = output_dir

    def fetch_stock_data(self) -> Dict[str, Dict[str, str]]:
        """Fetch daily stock data from Alpha Vantage API."""
        try:
            logger.info(f"Fetching stock data for symbol: {self.symbol}")
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': self.symbol,
                'apikey': self.api_key,  # API Key USED HERE in API request
                'outputsize': 'full',
                'datatype': 'json'
            }
            response = requests.get(self.url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'Time Series (Daily)' not in data:
                raise DataIngestionError("Time Series data not found in response.")

            logger.info("Stock data fetched successfully.")
            return data['Time Series (Daily)']
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise DataIngestionError(f"Failed to fetch stock data: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in fetching stock data: {str(e)}")
            raise DataIngestionError(str(e))

    def save_data_as_parquet(self, data: Dict[str, Dict[str, str]], filename: str) -> str:
        """Convert JSON data to DataFrame and save as Parquet."""
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            filepath = os.path.join(self.output_dir, filename)
            logger.info("Converting JSON data to DataFrame.")
            df = pd.DataFrame.from_dict(data, orient='index')
            df.index.name = 'Date'
            df.reset_index(inplace=True)
            df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            df = df.astype({'Open': 'float', 'High': 'float', 'Low': 'float',
                            'Close': 'float', 'Volume': 'int'})
            df.to_parquet(filepath, engine='pyarrow', index=False)
            logger.info(f"Data saved as parquet at {filepath}.")
            return filepath
        except Exception as e:
            logger.error(f"Error saving data as parquet: {str(e)}")
            raise DataIngestionError(f"Failed to save parquet: {str(e)}")

    def ingest(self) -> str:
        """Fetch stock data and save it as a Parquet file."""
        data = self.fetch_stock_data()
        filename = f"{self.symbol}_stock_data.parquet"
        return self.save_data_as_parquet(data, filename)
import os
import pandas as pd
from src.utils.logger import logger
from src.utils.exception import DataTransformationError
from src.config.config import DATA_DIR

class DataTransformation:
    def preprocess_data(self, df: pd.DataFrame, fill_method: str = 'ffill') -> pd.DataFrame:
        try:
            logger.info("Starting data preprocessing.")
            required_cols = {'Date', 'Open', 'High', 'Low', 'Close', 'Volume'}
            if not required_cols.issubset(df.columns):
                raise DataTransformationError(f"Missing required columns: {required_cols - set(df.columns)}")

            df = df.copy()
            df['Date'] = pd.to_datetime(df['Date'])
            df.sort_values(by='Date', inplace=True)
            if fill_method == 'ffill':
                df.ffill(inplace=True)
            elif fill_method == 'bfill':
                df.bfill(inplace=True)
            else:
                raise ValueError(f"Unsupported fill_method: {fill_method}")
            logger.info("Data preprocessing completed.")
            return df
        except Exception as e:
            logger.error(f"Error during preprocessing: {str(e)}")
            raise DataTransformationError(f"Preprocessing failed: {str(e)}")

    def transform_and_save(self, input_path: str, output_path: str) -> str:
        """Load raw data, preprocess it, and save to processed directory."""
        try:
            logger.info(f"Loading raw data from {input_path}")
            df = pd.read_parquet(input_path)
            processed_df = self.preprocess_data(df)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            processed_df.to_parquet(output_path, index=False)
            logger.info(f"Processed data saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error in transform_and_save: {str(e)}")
            raise DataTransformationError(f"Failed to save processed data: {str(e)}")

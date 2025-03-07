import os
import pandas as pd
from dotenv import load_dotenv
from src.stockml.data_ingestion import DataIngestion
from src.stockml.data_transformation import DataTransformation
from src.stockml.model_trainer import ModelTrainer
from src.utils.logger import logger
from src.utils.exception import DataIngestionError, DataTransformationError, CustomException
from src.config.config import API_KEY, DATA_DIR

# Load environment variables from .env file
load_dotenv()

SYMBOL = "IBM"
RAW_DIR = os.path.join(DATA_DIR, "..", "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "..", "processed")
MODEL_DIR = os.path.join(DATA_DIR, "..", "models")

def main():
    """Run data ingestion, preprocessing, and model training with comparison."""
    try:
        # Ingestion
        logger.info("Starting stock data ingestion process.")
        os.makedirs(RAW_DIR, exist_ok=True)
        ingestion = DataIngestion(API_KEY, SYMBOL, RAW_DIR)
        raw_filepath = ingestion.ingest()
        print(f"Stock data successfully downloaded and saved at: {raw_filepath}")

        # Preprocessing
        logger.info("Starting data preprocessing process.")
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        transformer = DataTransformation()
        processed_filepath = transformer.transform_and_save(
            input_path=raw_filepath,
            output_path=os.path.join(PROCESSED_DIR, f"{SYMBOL}_processed.parquet")
        )
        print(f"Processed data saved at: {processed_filepath}")

        # Load processed data
        df = pd.read_parquet(processed_filepath)
        
        # Feature selection
        X = df[['Open', 'High', 'Low', 'Volume']]
        y = df['Close']
        
        # Train-test split (80% train, 20% test)
        train_size = int(0.8 * len(df))
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        # Ensure models directory exists
        os.makedirs(MODEL_DIR, exist_ok=True)

        # Train and compare models
        model_types = ["lightgbm", "random_forest", "xgboost", "arima"]
        results = {}
        
        for model_type in model_types:
            trainer = ModelTrainer(model_type=model_type)
            model_path = os.path.join(MODEL_DIR, f"{model_type}_model.pkl")
            model, metrics = trainer.train(X_train, y_train, X_test, y_test, model_path=model_path)
            results[model_type] = metrics
        
        # Print comparison
        print("\nModel Performance Comparison:")
        for model_type, metrics in results.items():
            print(f"{model_type.upper()}:")
            print(f"  Train MSE: {metrics['train_mse']:.2f}, Test MSE: {metrics['test_mse']:.2f}")
            print(f"  Train R2: {metrics['train_r2']:.2f}, Test R2: {metrics['test_r2']:.2f}")
        
        logger.info("Pipeline completed successfully.")
    except DataIngestionError as e:
        print(f"Data ingestion failed: {str(e)}")
        logger.error(f"Data ingestion failed: {str(e)}")
    except DataTransformationError as e:
        print(f"Data transformation failed: {str(e)}")
        logger.error(f"Data transformation failed: {str(e)}")
    except CustomException as e:
        print(f"Model training failed: {str(e)}")
        logger.error(f"Model training failed: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
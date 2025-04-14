import sys
sys.path.append('/app')
import os
from airflow import DAG
from airflow.operators.python import PythonOPerator
from datetime import datetime,timedelta
from src.stockml.data_ingestion import DataIngestion
from src.stockml.data_transformation import DataTransformation
from src.stockml.model_trainer import ModelTrainer
from src.config.config import  API_KEY, DATA_DIR


default_args = {
    'owner': 'duncan',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


def fetch_data_task():
    ingestion = DataIngestion(api_key=API_KEY, symbol="IBM")
    raw_data_path = os.path.join("/app/data", "raw", "IBM_stock_data.parquet")
    ingestion.fetch_data(raw_data_path)

def transform_data_task():
    transformation = DataTransformation()
    raw_data_path = os.path.join("/app/data", "raw", "IBM_stock_data.parquet")
    processed_data_path = os.path.join("/app/data", "processed", "IBM_processed.parquet")
    transformation.transform_data(raw_data_path, processed_data_path)

def train_model_task():
    trainer = ModelTrainer()
    processed_data_path = os.path.join("/app/data", "processed", "IBM_processed.parquet")
    trainer.train_models(processed_data_path)

with DAG(
    'stockml_pipeline',
    default_args=default_args,
    description='Daily STOCKML pipeline for IBM stock prediction',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 3, 11),
    catchup=False
) as dag:
    fetch = PythonOperator(task_id='fetch_data', python_callable=fetch_data_task)
    transform = PythonOperator(task_id='transform_data', python_callable=transform_data_task)
    train = PythonOperator(task_id='train_model', python_callable=train_model_task)
    fetch >> transform >> train

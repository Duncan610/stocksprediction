import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
MODEL_DIR = os.path.join(DATA_DIR, "models")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
RAW_DIR = os.path.join(DATA_DIR, "raw")

# Alpha Vantage API
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")
if not API_KEY:
    raise ValueError("ALPHA_VANTAGE_API_KEY environment variable not set.")
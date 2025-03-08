## End to End ML Stock Price Prediction project

Predicts IBM stock prices using Random Forest, trained on Alpha Vantage data.

## Setup
1. Clone the repo: `git clone https://github.com/yourusername/STOCKML.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Get an API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).
4. Create `.env` with: `API_KEY=your_key_here`
5. Run `data_ingest.py` to fetch data and train models: `python data_ingest.py`
6. Run predictions: `python scripts/predict.py`

## Results
- Best Model: Random Forest (Test MSE: 45.82, R²: 0.96)
- See `notebooks/eda.ipynb` for visualization.

## Structure
- `data_ingest.py`: Pipeline script
- `scripts/predict.py`: 5-day forecast
- `src/`: Modules
- `notebooks/`: EDA
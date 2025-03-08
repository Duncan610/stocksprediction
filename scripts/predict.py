import pandas as pd
import pickle
import os
from src.config.config import DATA_DIR

MODEL_DIR = os.path.join(DATA_DIR, "..", "models")
PROCESSED_DIR = os.path.join(DATA_DIR, "..", "processed")

def load_model(model_path):
    with open(model_path, 'rb') as f:
        return pickle.load(f)

def predict_future(model, X_recent, days=5):
    predictions = []
    current_input = X_recent[-1:].copy()
    for _ in range(days):
        pred = model.predict(current_input)
        predictions.append(pred[0])
        # Shift: Update 'Volume' with predicted 'Close'
        current_input.iloc[0, -1] = pred[0]
    return predictions

def main():
    # Load processed data
    df = pd.read_parquet(os.path.join(PROCESSED_DIR, "IBM_processed.parquet"))
    X = df[['Open', 'High', 'Low', 'Volume']]
    
    # Load Random Forest model (best performer)
    model_path = os.path.join(MODEL_DIR, "random_forest_model.pkl")
    model = load_model(model_path)
    
    # Predict next 5 days
    predictions = predict_future(model, X)
    print("Predicted IBM stock prices for the next 5 days:")
    for i, pred in enumerate(predictions, 1):
        print(f"Day {i}: ${pred:.2f}")

if __name__ == "__main__":
    main()
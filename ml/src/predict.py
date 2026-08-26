import joblib
import pandas as pd
from .features import create_features

model = joblib.load("ml/models/linearRegressionModel.pkl")

def predict_price(file_path : str):

    df = create_features(file_path)

    X = df[
        [
            "ram_type",
            "form_factor",
            "previous_price",
            "prev_7_day_price",
            "prev_month_price",
            "prev_7_day_price_avg",
            "prev_month_price_avg",
            "price_diff_1_d",
            "prce_diff_1_d_pct",
            "7d_displacement"
        ]
    ]

    predictions = model.predict(X)
    predictions = predictions.round(4)

    results = pd.DataFrame(
        {
            "date" : df["date"],
            "ram_type" : df["ram_type"],
            "form_factor" : df["form_factor"],
            "actual_price" : df["avg_price_per_gb"],
            "predicted_price" : predictions
        }
    )

    return results


results = predict_price ("ml/data/raw/ramradar-price-index.csv")
print(results.head(30))
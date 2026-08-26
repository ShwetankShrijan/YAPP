import pandas as pd
from .preprocessing import cleanedData

def create_features(file_path: str) -> pd.DataFrame:
    df = cleanedData(file_path)

    df["previous_price"] = (
        df.groupby(
            ["ram_type", "form_factor"]
        )["avg_price_per_gb"].shift(1)
    )

    df["prev_7_day_price"] = (
        df.groupby(
            ["ram_type", "form_factor"]
        )["avg_price_per_gb"].shift(7)
    )

    df["prev_month_price"] = (
        df.groupby(
            ["ram_type", "form_factor"]
        )["avg_price_per_gb"].shift(30)
    )

    df["prev_7_day_price_avg"] = (
        df.groupby(
            ["ram_type", "form_factor"]
        )["avg_price_per_gb"].transform(lambda x : x.rolling(7).mean())
    )

    df["prev_month_price_avg"] = (
        df.groupby(
            ["ram_type", "form_factor"]
        )["avg_price_per_gb"].transform(lambda x : x.rolling(30).mean())
    )

    # LR could not understand sudden spikes and drops so i have to implement a price velocity and momentum feature so it understands
    # how fast or slow price changes 

    df["price_diff_1_d"] = (
        df.groupby(
            ["ram_type", "form_factor"]
        )["previous_price"].diff(1) # this is velocity feature price today - price yesterday
    )
    df["prce_diff_1_d_pct"] = (
        df.groupby(
            ["ram_type", "form_factor"]
        )["previous_price"].pct_change(1) # this is momentum feature
    )
    df["7d_displacement"] = df["previous_price"] - df["prev_7_day_price_avg"]

    df = df.dropna().reset_index(drop=True)

    return df
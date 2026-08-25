import pandas as pd
from preprocessing import cleanedData

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

    df = df.dropna().reset_index(drop=True)

    return df
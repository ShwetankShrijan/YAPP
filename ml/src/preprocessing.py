import pandas as pd
from sqlalchemy import create_engine
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PRICE_DB_URL: str
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
settings = Settings()
engine = create_engine(settings.PRICE_DB_URL)

# print(df.dtypes) # follow these steps when i had to process the data check the datatype
# print(df.isnull().sum()) # check if any column has no value and how many 
# print(df.duplicated().sum()) # check duplicates

# # then check all categorial values
# print(df["ram_type"].value_counts())
# print(df["form_factor"].value_counts())

# print(df.describe())

# To check the time slot of the entire dataset collected
# print("Start:", df["date"].min())
# print("End:", df["date"].max())

# print(
#     df.groupby(["ram_type", "form_factor"]).size()
# )

# df = df.sort_values("date") # sort the entire dataset in increasing order of date

def cleanedData(file_path : str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(
        ["ram_type", "form_factor", "date"]
    ).reset_index(drop=True) # to remove the NaN values since from starting we wont have 30 days data so we remove that using this line
    return df

# print(
#     df[
#         [
#             "date",
#             "ram_type",
#             "form_factor",
#             "avg_price_per_gb",
#             "previous_price",
#             "prev_7_day_price",
#             "prev_month_price",
#             "prev_7_day_price_avg",
#             "prev_month_price_avg"
#         ]
#     ].head(5)
# )

# print(df.isnull().sum())
# print(df.shape)
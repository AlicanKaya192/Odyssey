import os
import pandas as pd
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
for c in ["city", "category", "payment"]:
    df[c] = df[c].astype("category")

# Write in three formats.


# The CSV and Parquet sizes (MB).


# How many times smaller does gzip make the CSV?


# The CSV / Parquet ratio.

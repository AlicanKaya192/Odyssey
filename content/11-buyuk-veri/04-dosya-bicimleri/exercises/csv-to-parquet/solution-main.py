import os
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 300_000)

df = pd.read_csv(
    "orders.csv",
    dtype={"city": "category", "category": "category", "payment": "category",
           "quantity": "int8"},
    parse_dates=["order_time"],
)
df.to_parquet("orders.parquet", compression="zstd")

csv_mb = os.path.getsize("orders.csv") / 1024**2
parquet_mb = os.path.getsize("orders.parquet") / 1024**2
print(round(csv_mb, 1), round(parquet_mb, 1))
print(round(csv_mb / parquet_mb, 1))

back = pd.read_parquet("orders.parquet")
print(back.equals(df), (back.dtypes == df.dtypes).all())

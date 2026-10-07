import pandas as pd
from orders_data import make_orders

df = make_orders(20_000)
df["order_time"] = pd.to_datetime(df["order_time"])
for c in ["city", "category", "payment"]:
    df[c] = df[c].astype("category")

df.to_csv("orders.csv", index=False)
df.to_parquet("orders.parquet")

from_csv = pd.read_csv("orders.csv")
from_parquet = pd.read_parquet("orders.parquet")

print("csv", from_csv["order_time"].dtype, from_csv["city"].dtype)
print("parquet", from_parquet["order_time"].dtype, from_parquet["city"].dtype)

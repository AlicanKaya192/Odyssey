import os
import pandas as pd
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
for c in ["city", "category", "payment"]:
    df[c] = df[c].astype("category")

df.to_csv("orders.csv", index=False, lineterminator="\n")
df.to_csv("orders.csv.gz", index=False, lineterminator="\n")
df.to_parquet("orders.parquet")

for name in ["orders.csv", "orders.parquet"]:
    print(name, round(os.path.getsize(name) / 1024**2, 2))

print(round(os.path.getsize("orders.csv") / os.path.getsize("orders.csv.gz")))
print(round(os.path.getsize("orders.csv") / os.path.getsize("orders.parquet"), 1))

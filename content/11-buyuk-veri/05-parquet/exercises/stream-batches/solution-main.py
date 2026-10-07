import pandas as pd
import pyarrow.parquet as pq
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
df.to_parquet("orders.parquet", row_group_size=200_000)

f = pq.ParquetFile("orders.parquet")

parts = []
count = 0
for batch in f.iter_batches(batch_size=60_000, columns=["category", "quantity"]):
    part = batch.to_pandas()
    parts.append(part.groupby("category")["quantity"].sum())
    count += 1

totals = pd.concat(parts).groupby(level=0).sum().sort_values(ascending=False)
for category, quantity in totals.items():
    print(category, quantity)
print(count)

import pandas as pd
import pyarrow.parquet as pq
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
df.to_parquet("orders.parquet", row_group_size=20_000)

f = pq.ParquetFile("orders.parquet")
t = f.schema_arrow.names.index("order_time")

start = pd.Timestamp("2024-03-01")
end = pd.Timestamp("2024-04-01")

keep = []
for i in range(f.metadata.num_row_groups):
    stats = f.metadata.row_group(i).column(t).statistics
    if stats.max >= start and stats.min < end:
        keep.append(i)
print(keep)

read = pd.concat([f.read_row_group(i).to_pandas() for i in keep])
print(len(read))

march = read[(read["order_time"] >= start) & (read["order_time"] < end)]
print(len(march))

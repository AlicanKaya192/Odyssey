import pandas as pd
import pyarrow.parquet as pq
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
df.to_parquet("orders.parquet", row_group_size=40_000)

f = pq.ParquetFile("orders.parquet")

t = f.schema_arrow.names.index("order_time")

for i in range(f.metadata.num_row_groups):
    stats = f.metadata.row_group(i).column(t).statistics
    print(i, stats.min.date(), stats.max.date())

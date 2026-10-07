import pandas as pd
import pyarrow.parquet as pq
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
df.to_parquet("orders.parquet", row_group_size=50_000)

f = pq.ParquetFile("orders.parquet")
meta = f.metadata
print(meta.num_rows, meta.num_row_groups, meta.num_columns)
for name in f.schema_arrow.names:
    print(name)
print(meta.row_group(0).num_rows)

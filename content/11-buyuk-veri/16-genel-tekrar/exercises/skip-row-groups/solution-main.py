import pandas as pd
import pyarrow.parquet as pq
from orders_data import make_orders

make_orders(400_000).to_parquet("orders.parquet", row_group_size=50_000, index=False)
pf = pq.ParquetFile("orders.parquet")
col = pf.schema_arrow.names.index("order_time")

groups = []
for i in range(pf.num_row_groups):
    stats = pf.metadata.row_group(i).column(col).statistics
    if stats.max >= "2024-12":
        groups.append(i)

december = 0
for i in groups:
    part = pf.read_row_group(i, columns=["order_time"]).to_pandas()
    december += part["order_time"].str.startswith("2024-12").sum()

print(len(groups), pf.num_row_groups)
print(december)

everything = pd.read_parquet("orders.parquet", columns=["order_time"])
print(december == everything["order_time"].str.startswith("2024-12").sum())

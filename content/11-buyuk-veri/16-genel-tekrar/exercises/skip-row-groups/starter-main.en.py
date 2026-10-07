import pandas as pd
import pyarrow.parquet as pq
from orders_data import make_orders

make_orders(400_000).to_parquet("orders.parquet", row_group_size=50_000, index=False)
pf = pq.ParquetFile("orders.parquet")
col = pf.schema_arrow.names.index("order_time")

# 2. The groups that may contain December.


# 3-4. Read only those and count.


# 5. Compare with the whole file.

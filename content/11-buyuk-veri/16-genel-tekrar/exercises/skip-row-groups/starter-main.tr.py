import pandas as pd
import pyarrow.parquet as pq
from orders_data import make_orders

make_orders(400_000).to_parquet("orders.parquet", row_group_size=50_000, index=False)
pf = pq.ParquetFile("orders.parquet")
col = pf.schema_arrow.names.index("order_time")

# 2. Aralik'i icerebilecek gruplar.


# 3-4. Yalnizca onlari oku ve say.


# 5. Dosyanin tamamiyla karsilastir.

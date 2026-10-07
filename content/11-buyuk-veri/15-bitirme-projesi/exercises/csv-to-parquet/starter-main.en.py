import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 400_000)
NUMERIC = {"order_id": "int32", "customer_id": "int32", "quantity": "int8"}
MB = 1024**2

# 1-3. Write to Parquet piece by piece.
writer = None


# 4. Rows, row groups, sizes.


# 5. The number of different months.

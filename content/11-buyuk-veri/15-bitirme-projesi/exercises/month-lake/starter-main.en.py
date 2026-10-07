import os
import re
import duckdb
from orders_data import make_orders

orders = make_orders(300_000)
orders["month"] = orders["order_time"].str[:7]
LAKE = "read_parquet('lake/*/*.parquet', hive_partitioning = true)"

# 1-2. The month folders.


# 3. June's top three categories.


# 4. The files scanned.

import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(300_000)
orders["month"] = orders["order_time"].str[:7]
orders.to_parquet("orders.parquet", index=False)

# 2. The top three cities and their shares.


# 3. The month with the highest mean per order.


# 4. A quick estimate with a sample.

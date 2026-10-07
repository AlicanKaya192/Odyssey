import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])
orders.to_parquet("orders.parquet", index=False)

# DuckDB: revenue per month and payment method, .df().


# pandas: pivot and percentage shares.


# The card share of the first three months; the mean cash share.

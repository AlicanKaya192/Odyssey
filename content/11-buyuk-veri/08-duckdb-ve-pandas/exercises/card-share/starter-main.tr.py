import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])
orders.to_parquet("orders.parquet", index=False)

# DuckDB: ay ve odeme turu basina ciro, .df().


# pandas: pivot ve yuzde paylar.


# Ilk uc ayin kart payi; nakit payinin ortalamasi.

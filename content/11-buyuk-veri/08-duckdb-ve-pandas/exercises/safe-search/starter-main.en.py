import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(100_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])
orders.to_parquet("orders.parquet", index=False)


def count_orders(city, min_quantity):
    # A query with two ? parameters.
    pass


# Three calls.

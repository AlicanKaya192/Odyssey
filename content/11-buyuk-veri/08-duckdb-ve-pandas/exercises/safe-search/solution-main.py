import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(100_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])
orders.to_parquet("orders.parquet", index=False)


def count_orders(city, min_quantity):
    query = "SELECT count(*) FROM 'orders.parquet' WHERE city = ? AND quantity >= ?"
    return duckdb.execute(query, [city, min_quantity]).fetchone()[0]


print(count_orders("Izmir", 3))
print(count_orders("Bursa", 5))
print(count_orders("Izmir' OR '1'='1", 1))

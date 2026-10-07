import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(100_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])
orders.to_parquet("orders.parquet", index=False)

first = duckdb.sql("""
    SELECT customer_id, order_id, order_time
    FROM 'orders.parquet'
    QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY order_time) = 1
""")

print(duckdb.sql("SELECT count(*) FROM first").fetchone()[0])
print(duckdb.sql("SELECT count(*) FROM first WHERE month(order_time) = 1").fetchone()[0])
for customer_id, order_id in duckdb.sql(
        "SELECT customer_id, order_id FROM first ORDER BY customer_id LIMIT 3").fetchall():
    print(customer_id, order_id)

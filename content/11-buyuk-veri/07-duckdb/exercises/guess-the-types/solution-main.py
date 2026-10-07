import duckdb
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 50_000)

rows = duckdb.sql("""
    SELECT column_name, column_type
    FROM (DESCRIBE SELECT * FROM 'orders.csv')
""").fetchall()
for name, kind in rows:
    print(name, kind)

print(pd.read_csv("orders.csv")["order_time"].dtype)

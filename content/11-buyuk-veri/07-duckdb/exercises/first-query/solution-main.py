import duckdb
from orders_data import make_orders

make_orders(100_000).to_parquet("orders.parquet", index=False)

row = duckdb.sql("""
    SELECT count(*), count(DISTINCT city), sum(quantity)
    FROM 'orders.parquet'
""").fetchone()

for value in row:
    print(value)

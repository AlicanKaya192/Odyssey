import duckdb
from orders_data import make_orders

df = make_orders(100_000)

rows = duckdb.sql("""
    SELECT payment, count(*) AS orders
    FROM df
    GROUP BY payment
    ORDER BY orders DESC
""").fetchall()
for payment, orders in rows:
    print(payment, orders)

import duckdb
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 200_000)

rows = duckdb.sql("""
    SELECT category, count(*) AS orders, round(avg(unit_price), 2) AS avg_price
    FROM 'orders.csv'
    GROUP BY category
    ORDER BY orders DESC
""").fetchall()

for category, orders, avg_price in rows:
    print(category, orders, avg_price)

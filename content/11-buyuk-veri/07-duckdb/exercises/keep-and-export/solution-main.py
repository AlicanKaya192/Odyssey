import duckdb
from orders_data import make_orders

make_orders(100_000).to_parquet("orders.parquet", index=False)

con = duckdb.connect("shop.duckdb")
con.sql("CREATE TABLE orders AS SELECT * FROM 'orders.parquet'")
con.sql("""
    CREATE TABLE city_summary AS
    SELECT city, count(*) AS orders, round(sum(quantity * unit_price), 2) AS revenue
    FROM orders
    GROUP BY city
    ORDER BY city
""")
con.sql("COPY city_summary TO 'city_summary.csv' (HEADER)")
con.close()

con = duckdb.connect("shop.duckdb")
print(con.sql("SELECT count(*) FROM orders").fetchone()[0])
con.close()

with open("city_summary.csv") as f:
    for line in f.read().splitlines()[:3]:
        print(line)

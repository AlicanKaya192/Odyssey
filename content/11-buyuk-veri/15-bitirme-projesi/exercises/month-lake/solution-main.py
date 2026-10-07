import os
import re
import duckdb
from orders_data import make_orders

orders = make_orders(300_000)
orders["month"] = orders["order_time"].str[:7]
LAKE = "read_parquet('lake/*/*.parquet', hive_partitioning = true)"

for month, part in orders.groupby("month"):
    folder = f"lake/month={month}"
    os.makedirs(folder, exist_ok=True)
    part.drop(columns="month").to_parquet(f"{folder}/part-0.parquet", index=False)
print(len(os.listdir("lake")))

rows = duckdb.sql(f"""
    SELECT category, round(sum(quantity * unit_price), 2) AS revenue
    FROM {LAKE}
    WHERE month = '2024-06'
    GROUP BY category
    ORDER BY revenue DESC
    LIMIT 3
""").fetchall()
for category, revenue in rows:
    print(category, revenue)

plan = duckdb.sql(f"""
    EXPLAIN ANALYZE SELECT count(*) FROM {LAKE} WHERE month = '2024-06'
""").fetchall()[0][1]
print(re.search(r"Scanning Files: \d+/\d+", plan).group())

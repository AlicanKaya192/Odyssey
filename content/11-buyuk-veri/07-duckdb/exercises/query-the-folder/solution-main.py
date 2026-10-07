import duckdb
from pathlib import Path
import pandas as pd
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
df["month"] = df["order_time"].dt.strftime("%Y-%m")
for month, part in df.groupby("month"):
    folder = Path("orders") / f"month={month}"
    folder.mkdir(parents=True, exist_ok=True)
    part.drop(columns="month").to_parquet(folder / "part-0.parquet", index=False)

print(duckdb.sql("SELECT count(*) FROM 'orders/*/*.parquet'").fetchone()[0])

rows = duckdb.sql("""
    SELECT month, count(*) AS orders
    FROM read_parquet('orders/*/*.parquet', hive_partitioning = true)
    WHERE month <= '2024-03'
    GROUP BY month
    ORDER BY month
""").fetchall()
for month, orders in rows:
    print(month, orders)

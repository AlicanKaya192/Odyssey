import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(300_000)
orders["month"] = orders["order_time"].str[:7]
orders.to_parquet("orders.parquet", index=False)

rows = duckdb.sql("""
    SELECT city,
           round(100 * sum(quantity * unit_price)
                 / (SELECT sum(quantity * unit_price) FROM 'orders.parquet'), 1) AS share
    FROM 'orders.parquet'
    GROUP BY city
    ORDER BY share DESC
    LIMIT 3
""").fetchall()
for city, share in rows:
    print(city, share)

month, mean = duckdb.sql("""
    SELECT month, round(avg(quantity * unit_price), 2) AS mean
    FROM 'orders.parquet'
    GROUP BY month
    ORDER BY mean DESC
    LIMIT 1
""").fetchone()
print(month, mean)

data = pd.read_parquet("orders.parquet")
data["revenue"] = data["quantity"] * data["unit_price"]
estimate = data.sample(frac=0.01, random_state=3)["revenue"].mean()
true = data["revenue"].mean()
print(round(estimate, 2), round(true, 2), round(abs(estimate - true) / true * 100, 1))

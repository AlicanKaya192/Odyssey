import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])
orders.to_parquet("orders.parquet", index=False)

monthly = duckdb.sql("""
    SELECT strftime(order_time, '%Y-%m') AS month, payment,
           sum(quantity * unit_price) AS revenue
    FROM 'orders.parquet'
    GROUP BY month, payment
""").df()

table = monthly.pivot(index="month", columns="payment", values="revenue")
share = table.div(table.sum(axis=1), axis=0) * 100

for month, value in share["card"].head(3).items():
    print(month, round(value, 1))
print(round(share["cash"].mean(), 1))

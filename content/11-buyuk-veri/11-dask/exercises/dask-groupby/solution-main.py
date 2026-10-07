import dask
import dask.dataframe as dd
import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
for i in range(4):
    orders.iloc[i * 50_000:(i + 1) * 50_000].to_csv(f"orders-{i}.csv", index=False)

ddf = dd.read_csv("orders-*.csv")
by_payment = ddf.groupby("payment")["quantity"].sum().compute().sort_index()
for payment, quantity in by_payment.items():
    print(payment, quantity)

expected = orders.groupby("payment")["quantity"].sum().sort_index()
print(by_payment.equals(expected))

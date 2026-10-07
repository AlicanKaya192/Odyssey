import dask
import dask.dataframe as dd
import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
for i in range(4):
    orders.iloc[i * 50_000:(i + 1) * 50_000].to_csv(f"orders-{i}.csv", index=False)

ddf = dd.read_csv("orders-*.csv")
print(ddf.npartitions)

total = ddf["quantity"].sum()
print(type(total).__name__)
print(total.compute())

print(len(ddf))

import dask
import dask.dataframe as dd
import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
for i in range(4):
    orders.iloc[i * 50_000:(i + 1) * 50_000].to_csv(f"orders-{i}.csv", index=False)

# dask: total quantity per payment method.


# The same with pandas, and the comparison.

import dask
import dask.dataframe as dd
import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
for i in range(4):
    orders.iloc[i * 50_000:(i + 1) * 50_000].to_csv(f"orders-{i}.csv", index=False)
from dask import delayed


def file_revenue(path):
    part = pd.read_csv(path)
    return (part["quantity"] * part["unit_price"]).sum()


parts = [delayed(file_revenue)(f"orders-{i}.csv") for i in range(4)]
total = delayed(sum)(parts)

print(type(total).__name__)
print(round(total.compute(), 2))

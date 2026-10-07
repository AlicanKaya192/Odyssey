import dask
import dask.dataframe as dd
import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
for i in range(4):
    orders.iloc[i * 50_000:(i + 1) * 50_000].to_csv(f"orders-{i}.csv", index=False)

ddf = dd.read_csv("orders-*.csv")

mean_price = ddf["unit_price"].mean()
big_orders = ddf[ddf["quantity"] >= 4].shape[0]
cities = ddf["city"].nunique()

mean_value, big_count, city_count = dask.compute(mean_price, big_orders, cities)
print(round(mean_value, 2))
print(big_count)
print(city_count)

import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])

samples = [("head", orders.head(5_000)),
           ("random", orders.sample(n=5_000, random_state=0))]

for name, part in samples:
    t = part["order_time"]
    print(name, t.dt.month.nunique(), t.min().date(), t.max().date())

for name, part in samples:
    print(name, part["order_time"].dt.date.nunique())

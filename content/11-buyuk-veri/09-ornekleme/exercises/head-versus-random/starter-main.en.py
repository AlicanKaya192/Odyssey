import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])

# Two samples: head and random.


# Number of months and the date range.


# Number of different days.

import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 200_000)
orders = pd.read_csv("orders.csv")
MB = 1024**2

# 1. Memory with the default types.


# 2-4. The shrunk copy, its memory and the new types.


# 5. Are the revenue totals the same?

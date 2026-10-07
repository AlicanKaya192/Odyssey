import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 20_000)
df = pd.read_csv("orders.csv")

# Numeric and text columns.


# Memory of both groups (index left out).


# Percentage shares.


# Bytes per row.

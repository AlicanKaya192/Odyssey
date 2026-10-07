from pathlib import Path
import pandas as pd
from orders_data import make_orders

df = make_orders(50_000)
df["order_time"] = pd.to_datetime(df["order_time"])

# The month and day columns.


# Write by month and by day.


# Each layout: name, number of files, total KB.


# The ratio.

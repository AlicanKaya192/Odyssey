import pandas as pd
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
for c in ["city", "category", "payment"]:
    df[c] = df[c].astype("category")

# Write as Parquet.


# Read only two columns; the column list.


# Both memories (MB).


# Mean price per city: the top three.

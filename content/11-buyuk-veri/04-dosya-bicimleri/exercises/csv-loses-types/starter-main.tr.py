import pandas as pd
from orders_data import make_orders

df = make_orders(20_000)
df["order_time"] = pd.to_datetime(df["order_time"])
for c in ["city", "category", "payment"]:
    df[c] = df[c].astype("category")

# CSV ve Parquet olarak yaz.


# Geri oku ve iki sutunun turunu yazdir.

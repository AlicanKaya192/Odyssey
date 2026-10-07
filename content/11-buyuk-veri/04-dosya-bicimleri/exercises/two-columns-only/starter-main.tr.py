import pandas as pd
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
for c in ["city", "category", "payment"]:
    df[c] = df[c].astype("category")

# Parquet olarak yaz.


# Yalnizca iki sutunu oku; sutun listesi.


# Iki bellek (MB).


# Sehir basina ortalama fiyat: ilk uc.

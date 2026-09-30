import pandas as pd

orders = pd.read_csv("orders_raw.csv")
orders["ordered"] = pd.to_datetime(orders["ordered_at"],
                                   format="%d.%m.%Y %H:%M", errors="coerce")

broken = orders["ordered"].isna()
print(int(broken.sum()))
print(orders.loc[broken, "ordered_at"].tolist())

orders = orders.dropna(subset=["ordered"])
print(len(orders))
print(orders["ordered"].min())

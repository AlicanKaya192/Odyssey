import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 200_000)

parts = []
for chunk in pd.read_csv("orders.csv", chunksize=50_000):
    chunk["revenue"] = chunk["quantity"] * chunk["unit_price"]
    parts.append(chunk.groupby("payment")["revenue"].sum())

combined = pd.concat(parts).groupby(level=0).sum().sort_values(ascending=False)
for payment, revenue in combined.items():
    print(payment, round(revenue / 1e6, 2))

df = pd.read_csv("orders.csv")
df["revenue"] = df["quantity"] * df["unit_price"]
full = df.groupby("payment")["revenue"].sum()
print((combined.round(2) == full.round(2).reindex(combined.index)).all())

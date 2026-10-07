import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 200_000)

tops = []
first = True
for chunk in pd.read_csv("orders.csv", chunksize=50_000):
    chunk["revenue"] = chunk["quantity"] * chunk["unit_price"]
    tops.append(chunk.nlargest(3, "revenue"))
    large = chunk[chunk["revenue"] >= 20_000]
    large.to_csv("large.csv", mode="w" if first else "a", header=first, index=False)
    first = False

top = pd.concat(tops).nlargest(3, "revenue")
for order_id, revenue in zip(top["order_id"], top["revenue"]):
    print(order_id, round(revenue, 2))

saved = pd.read_csv("large.csv")
print(len(saved), round(saved["revenue"].min(), 2))

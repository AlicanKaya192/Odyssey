import os
import pandas as pd
from orders_data import make_orders

small = make_orders(4)[["order_id", "quantity"]]
small.to_json("orders.jsonl", orient="records", lines=True)

with open("orders.jsonl") as f:
    lines = f.read().splitlines()
print(len(lines))
print(lines[0])

back = pd.read_json("orders.jsonl", lines=True)
print(back.shape, back["quantity"].sum())

big = make_orders(50_000)
big.to_json("big.jsonl", orient="records", lines=True)
big.to_csv("big.csv", index=False)
print(round(os.path.getsize("big.jsonl") / os.path.getsize("big.csv"), 2))

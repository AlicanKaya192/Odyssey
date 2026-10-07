import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 200_000)

seen = set()
wrong = 0
for chunk in pd.read_csv("orders.csv", chunksize=50_000, usecols=["customer_id"]):
    seen.update(chunk["customer_id"])
    wrong += chunk["customer_id"].nunique()

print(len(seen))
print(wrong)
print(round(wrong / len(seen), 2))

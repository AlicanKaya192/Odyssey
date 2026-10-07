import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 200_000)

means = []
total = 0
count = 0
for chunk in pd.read_csv("orders.csv", chunksize=70_000):
    means.append(chunk["quantity"].mean())
    total += chunk["quantity"].sum()
    count += len(chunk)

print(round(float(sum(means) / len(means)), 4))
print(round(float(total / count), 4))

print(round(float(pd.read_csv("orders.csv")["quantity"].mean()), 4))

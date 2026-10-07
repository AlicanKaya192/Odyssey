import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 100_000)

sizes = []
for chunk in pd.read_csv("orders.csv", chunksize=30_000):
    sizes.append(len(chunk))

print(sizes)
print(sum(sizes), len(sizes))

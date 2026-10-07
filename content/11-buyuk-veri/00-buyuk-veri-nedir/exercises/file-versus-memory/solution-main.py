import os
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 100_000)
df = pd.read_csv("orders.csv")

print(len(df))

file_bytes = os.path.getsize("orders.csv")
memory = df.memory_usage(deep=True)
memory_bytes = memory.sum()
print(round(file_bytes / 1024**2, 1), round(memory_bytes / 1024**2, 1))

print(round(memory_bytes / file_bytes, 2))

print(memory.drop("Index").idxmax())

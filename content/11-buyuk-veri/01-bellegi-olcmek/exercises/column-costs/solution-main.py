import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 20_000)
df = pd.read_csv("orders.csv")

memory = df.memory_usage(deep=True).drop("Index")
top = memory.sort_values(ascending=False).head(3)
for name, size in top.items():
    print(name, round(size / 1024, 1))

print(round(memory.sum() / 1024, 1))

import os
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 200_000)
DTYPES = {"order_id": "int32", "customer_id": "int32", "quantity": "int8",
          "city": "category", "category": "category", "payment": "category"}
MB = 1024**2

print(round(os.path.getsize("orders.csv") / MB, 1))

sample = pd.read_csv("orders.csv", nrows=5_000, dtype=DTYPES)
estimate = sample.memory_usage(deep=True).sum() / len(sample) * 200_000 / MB
print(round(estimate, 1))

full = pd.read_csv("orders.csv", dtype=DTYPES)
real = full.memory_usage(deep=True).sum() / MB
print(round(real, 1))
print(abs(estimate - real) / real < 0.02)

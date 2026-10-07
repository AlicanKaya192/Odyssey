import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 20_000)

df = pd.read_csv("orders.csv", dtype={"payment": object})

shallow = df["payment"].memory_usage()
deep = df["payment"].memory_usage(deep=True)
print(shallow, deep)

print(df["quantity"].memory_usage(), df["quantity"].memory_usage(deep=True))

print(round(deep / shallow, 1))

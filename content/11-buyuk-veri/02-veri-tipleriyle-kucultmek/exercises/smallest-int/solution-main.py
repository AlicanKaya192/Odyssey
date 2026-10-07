import pandas as pd
from orders_data import make_orders

df = make_orders(100_000)

for name in ["quantity", "customer_id", "order_id"]:
    column = df[name]
    small = pd.to_numeric(column, downcast="integer")
    print(name, column.min(), column.max(), small.dtype)

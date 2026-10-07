import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 200_000)
orders = pd.read_csv("orders.csv")
MB = 1024**2

print(round(orders.memory_usage(deep=True).sum() / MB, 1))

small = orders.copy()
for column in ["order_id", "customer_id", "quantity"]:
    small[column] = pd.to_numeric(small[column], downcast="integer")
for column in ["city", "category", "payment"]:
    small[column] = small[column].astype("category")

print(round(small.memory_usage(deep=True).sum() / MB, 1))
print(small["quantity"].dtype, small["customer_id"].dtype)

before = (orders["quantity"] * orders["unit_price"]).sum()
after = (small["quantity"] * small["unit_price"]).sum()
print(before == after)

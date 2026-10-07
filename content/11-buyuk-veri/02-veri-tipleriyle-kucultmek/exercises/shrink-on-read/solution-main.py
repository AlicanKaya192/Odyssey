import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 200_000)

plain = pd.read_csv("orders.csv")
typed = pd.read_csv(
    "orders.csv",
    dtype={"order_id": "int32", "customer_id": "int32", "quantity": "int8",
           "unit_price": "float32", "city": "category", "category": "category",
           "payment": "category"},
    parse_dates=["order_time"],
)

plain_mb = plain.memory_usage(deep=True).sum() / 1024**2
typed_mb = typed.memory_usage(deep=True).sum() / 1024**2
print(round(plain_mb, 1), round(typed_mb, 1))
print(round(plain_mb / typed_mb, 1))
print(typed["order_time"].dtype, typed["city"].dtype)

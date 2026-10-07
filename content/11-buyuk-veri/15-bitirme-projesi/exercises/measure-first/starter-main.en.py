import os
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 200_000)
DTYPES = {"order_id": "int32", "customer_id": "int32", "quantity": "int8",
          "city": "category", "category": "category", "payment": "category"}
MB = 1024**2

# 1. The size on disk.


# 2. The estimate from a 5000-row sample.


# 3. The real memory and 4. the comparison.

import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 400_000)
NUMERIC = {"order_id": "int32", "customer_id": "int32", "quantity": "int8"}
MB = 1024**2

# 1-3. Parca parca Parquet'e yaz.
writer = None


# 4. Satir, satir grubu, boyutlar.


# 5. Farkli ay sayisi.

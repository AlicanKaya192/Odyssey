import pandas as pd
import pyarrow.parquet as pq
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
df.to_parquet("orders.parquet", row_group_size=50_000)

# Dosyayi ac.


# Satir, grup ve sutun sayisi.


# Sutun adlari.


# Ilk grubun satir sayisi.

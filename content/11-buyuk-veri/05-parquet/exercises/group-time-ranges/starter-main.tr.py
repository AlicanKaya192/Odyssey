import pandas as pd
import pyarrow.parquet as pq
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
df.to_parquet("orders.parquet", row_group_size=40_000)

f = pq.ParquetFile("orders.parquet")

# order_time sutununun sirasi.


# Her grup: numara, en kucuk tarih, en buyuk tarih.

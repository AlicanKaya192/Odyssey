import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(100_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])
orders.to_parquet("orders.parquet", index=False)

# Her musterinin ilk siparisi: first.


# Musteri sayisi, Ocak'ta ilk siparisi olanlar, en kucuk uc musteri.

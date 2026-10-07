import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])
orders.to_parquet("orders.parquet", index=False)

ids = pd.RangeIndex(1, 50_000)
customers = pd.DataFrame({
    "customer_id": ids,
    "segment": pd.Series(["new", "regular", "vip"]).iloc[ids % 3].values,
})

# Siparisleri musterilerle birlestir: segment basina siparis ve ciro.

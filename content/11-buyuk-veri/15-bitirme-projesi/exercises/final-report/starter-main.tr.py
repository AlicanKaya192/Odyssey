import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(300_000)
orders["month"] = orders["order_time"].str[:7]
orders.to_parquet("orders.parquet", index=False)

# 2. Ilk uc sehir ve paylari.


# 3. Siparis basina ortalamanin en yuksek oldugu ay.


# 4. Orneklemle hizli tahmin.

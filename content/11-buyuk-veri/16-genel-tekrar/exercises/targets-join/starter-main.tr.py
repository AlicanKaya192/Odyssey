import duckdb
import pandas as pd
from orders_data import make_orders

orders = make_orders(300_000)
orders["month"] = orders["order_time"].str[:7]
orders.to_parquet("orders.parquet", index=False)

targets = pd.DataFrame({
    "city": ["Istanbul", "Ankara", "Izmir", "Bursa",
             "Antalya", "Konya", "Adana", "Trabzon"],
    "target": [14_000_000, 6_000_000, 5_000_000, 4_000_000,
               3_500_000, 3_000_000, 3_000_000, 2_000_000],
})
MONTH = "2024-03"

# Sorgu: aylik ciro, hedeflerle birlestirme, hedefe ulasanlar.


# Sonuclar.

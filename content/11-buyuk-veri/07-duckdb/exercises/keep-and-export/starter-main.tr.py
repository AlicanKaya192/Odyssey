import duckdb
from orders_data import make_orders

make_orders(100_000).to_parquet("orders.parquet", index=False)

# Baglan, orders ve city_summary tablolarini kur.


# city_summary'yi CSV'ye yaz, kapat.


# Yeniden baglan: orders satir sayisi.


# CSV'nin ilk uc satiri.

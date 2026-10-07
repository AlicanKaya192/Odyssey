import duckdb
from orders_data import make_orders

make_orders(100_000).to_parquet("orders.parquet", index=False)

# Tek sorgu: siparis sayisi, farkli sehir, toplam adet.


# Uc deger, ayri satirlarda.

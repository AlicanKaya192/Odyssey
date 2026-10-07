import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 200_000)
orders = pd.read_csv("orders.csv")
MB = 1024**2

# 1. Varsayilan turlerle bellek.


# 2-4. Kucultulmus kopya, bellegi ve yeni turler.


# 5. Ciro toplamlari ayni mi?

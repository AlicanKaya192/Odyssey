import pandas as pd
from orders_data import make_orders

orders = make_orders(200_000)
orders["order_time"] = pd.to_datetime(orders["order_time"])

# Iki orneklem: head ve rastgele.


# Ay sayisi ve tarih araligi.


# Farkli gun sayisi.

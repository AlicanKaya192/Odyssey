from pathlib import Path
import pandas as pd
from orders_data import make_orders

df = make_orders(50_000)
df["order_time"] = pd.to_datetime(df["order_time"])

# month ve day sutunlari.


# Aya gore ve gune gore yaz.


# Her duzen: ad, dosya sayisi, toplam KB.


# Oran.

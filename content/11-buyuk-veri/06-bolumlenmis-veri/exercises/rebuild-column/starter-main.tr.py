from pathlib import Path
import pandas as pd
from orders_data import make_orders

df = make_orders(100_000)
for payment, part in df.groupby("payment"):
    folder = Path("orders") / f"payment={payment}"
    folder.mkdir(parents=True, exist_ok=True)
    part.drop(columns="payment").to_parquet(folder / "part-0.parquet", index=False)

# Dosyalari gez, payment sutununu klasor adindan ekle.


# Odeme turu basina satir sayisi ve toplam.

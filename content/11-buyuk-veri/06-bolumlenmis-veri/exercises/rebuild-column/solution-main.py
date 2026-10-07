from pathlib import Path
import pandas as pd
from orders_data import make_orders

df = make_orders(100_000)
for payment, part in df.groupby("payment"):
    folder = Path("orders") / f"payment={payment}"
    folder.mkdir(parents=True, exist_ok=True)
    part.drop(columns="payment").to_parquet(folder / "part-0.parquet", index=False)

parts = []
for f in sorted(Path("orders").glob("payment=*/*.parquet")):
    piece = pd.read_parquet(f)
    piece["payment"] = f.parent.name.split("=")[1]
    parts.append(piece)

orders = pd.concat(parts, ignore_index=True)
for payment, count in orders.groupby("payment").size().items():
    print(payment, count)
print(len(orders))

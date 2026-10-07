from pathlib import Path
import pandas as pd
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
df["month"] = df["order_time"].dt.strftime("%Y-%m")
for month, part in df.groupby("month"):
    folder = Path("orders") / f"month={month}"
    folder.mkdir(parents=True, exist_ok=True)
    part.drop(columns="month").to_parquet(folder / "part-0.parquet", index=False)

june = pd.read_parquet("orders/month=2024-06/part-0.parquet")
print(len(june), round((june["quantity"] * june["unit_price"]).sum(), 2))

files = sorted(Path("orders").glob("month=*/*.parquet"))
everything = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
print(len(files))

june2 = everything[everything["order_time"].dt.month == 6]
print(len(june) == len(june2))

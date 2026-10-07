from pathlib import Path
import pandas as pd
from orders_data import make_orders

df = make_orders(50_000)
df["order_time"] = pd.to_datetime(df["order_time"])

df["month"] = df["order_time"].dt.strftime("%Y-%m")
df["day"] = df["order_time"].dt.strftime("%Y-%m-%d")

for column, root in [("month", "by_month"), ("day", "by_day")]:
    for value, part in df.groupby(column):
        folder = Path(root) / f"{column}={value}"
        folder.mkdir(parents=True, exist_ok=True)
        part.drop(columns=["month", "day"]).to_parquet(folder / "part-0.parquet", index=False)

totals = {}
for root in ["by_month", "by_day"]:
    files = list(Path(root).rglob("*.parquet"))
    totals[root] = sum(f.stat().st_size for f in files)
    print(root, len(files), round(totals[root] / 1024, 1))

print(round(totals["by_day"] / totals["by_month"], 2))

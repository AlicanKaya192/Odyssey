import duckdb
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

# The number of orders across all files.


# The first quarter: orders per month.

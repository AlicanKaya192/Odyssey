from pathlib import Path
import pandas as pd
from orders_data import make_orders

df = make_orders(200_000)

df["bucket"] = df["customer_id"] % 4
for bucket, part in df.groupby("bucket"):
    folder = Path("buckets") / f"bucket={bucket}"
    folder.mkdir(parents=True, exist_ok=True)
    part.drop(columns="bucket").to_parquet(folder / "part-0.parquet", index=False)

customer = 1234
bucket = customer % 4
print(bucket)

piece = pd.read_parquet(Path("buckets") / f"bucket={bucket}" / "part-0.parquet")
print(len(piece))

found = (piece["customer_id"] == customer).sum()
print(found)

print(found == (df["customer_id"] == customer).sum())

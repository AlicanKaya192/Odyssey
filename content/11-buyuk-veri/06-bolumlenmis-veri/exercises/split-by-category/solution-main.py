from pathlib import Path
from orders_data import make_orders

df = make_orders(100_000)

for category, part in df.groupby("category"):
    folder = Path("by_category") / f"category={category}"
    folder.mkdir(parents=True, exist_ok=True)
    part.drop(columns="category").to_parquet(folder / "part-0.parquet", index=False)

names = sorted(p.name for p in Path("by_category").iterdir())
for name in names:
    print(name)
print(len(names))

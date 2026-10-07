import pandas as pd
from orders_data import make_orders

df = make_orders(200_000)
df["order_time"] = pd.to_datetime(df["order_time"])
for c in ["city", "category", "payment"]:
    df[c] = df[c].astype("category")

df.to_parquet("orders.parquet")

prices = pd.read_parquet("orders.parquet", columns=["city", "unit_price"])
print(list(prices.columns))

full = pd.read_parquet("orders.parquet")
print(round(prices.memory_usage(deep=True).sum() / 1024**2, 1),
      round(full.memory_usage(deep=True).sum() / 1024**2, 1))

means = prices.groupby("city", observed=True)["unit_price"].mean().sort_values(ascending=False)
for city, mean in means.head(3).items():
    print(city, round(mean, 1))

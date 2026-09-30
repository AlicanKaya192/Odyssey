import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])

a = long[long["store"] == "A"][["date", "sales"]].sort_values("date")
prices = pd.read_csv("prices.csv", parse_dates=["valid_from"])

exact = a.merge(prices, left_on="date", right_on="valid_from", how="left")
print(int(exact["price"].notna().sum()))

joined = pd.merge_asof(a, prices, left_on="date", right_on="valid_from")
march = joined[joined["date"].between("2024-03-14", "2024-03-16")]
print(march["price"].tolist())

joined["revenue"] = joined["sales"] * joined["price"]
print(round(float(joined["revenue"].sum()), 1))
print(joined["price"].value_counts().sort_index().to_dict())

import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])
print(long.groupby("store").size().to_dict())

wide = long.pivot(index="date", columns="store", values="sales")
print(wide.shape)
print(wide.isna().sum().to_dict())
print(wide["D"].first_valid_index().strftime("%Y-%m-%d"))

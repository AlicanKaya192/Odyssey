import pandas as pd

messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]
fixed = messy.sort_index().groupby(level=0).sum()

full = pd.date_range(fixed.index.min(), fixed.index.max(), freq="D")
missing = full.difference(fixed.index)
print(len(missing))
print(missing.strftime("%Y-%m-%d").tolist())

print(fixed.index.to_series().diff().max().days)

regular = fixed.asfreq("D")
print(len(regular), int(regular.isna().sum()))

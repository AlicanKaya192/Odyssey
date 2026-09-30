import pandas as pd

messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]
fixed = messy.sort_index().groupby(level=0).sum()

rows = fixed.diff()
print(rows.loc["2024-07-18"])

position = fixed.index.get_loc(pd.Timestamp("2024-07-18"))
print(fixed.index[position - 1].strftime("%Y-%m-%d"))

days = fixed.asfreq("D").diff()
print(days.loc["2024-07-18"])

print(int(rows.isna().sum()), int(days.isna().sum()))

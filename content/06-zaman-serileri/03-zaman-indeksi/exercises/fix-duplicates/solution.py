import pandas as pd

messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]
messy = messy.sort_index()

repeated = messy.index.duplicated()
print(int(repeated.sum()))
print(messy.index[repeated].strftime("%Y-%m-%d").tolist())
print(messy.loc["2024-03-05"].tolist())

fixed = messy.groupby(level=0).sum()
print(len(fixed), fixed.index.is_unique)
print(fixed.loc["2024-03-05"])

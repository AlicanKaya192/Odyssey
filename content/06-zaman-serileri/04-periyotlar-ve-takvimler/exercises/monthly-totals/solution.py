import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

monthly = s.groupby(s.index.to_period("M")).sum()

print(len(monthly))
print(monthly.loc["2024-03"])
print(monthly.idxmax(), monthly.max())

import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

weekly = s.resample("W").sum()
counts = s.resample("W").count()

print(weekly.iloc[0], counts.iloc[0])

full = weekly[counts == 7]
print(len(weekly), len(full))

print(full.idxmax().strftime("%Y-%m-%d"), full.max())
print(full.idxmin().strftime("%Y-%m-%d"), full.min())

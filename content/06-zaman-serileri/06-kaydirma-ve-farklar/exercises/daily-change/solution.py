import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

change = s.diff()
print(round(float(change.abs().mean()), 1))
print(change.idxmax().strftime("%Y-%m-%d"), change.max())
print(change.idxmin().strftime("%Y-%m-%d"), change.min())

weekly_change = s.diff(7)
print(weekly_change.loc["2024-03-09"])
print(round(float(change.std()), 1), round(float(weekly_change.std()), 1))

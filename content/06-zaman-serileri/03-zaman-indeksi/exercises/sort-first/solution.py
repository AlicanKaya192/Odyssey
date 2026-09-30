import pandas as pd

messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]

print(messy.index.is_monotonic_increasing)
messy = messy.sort_index()
print(messy.index.is_monotonic_increasing)

print(messy.index[0].strftime("%Y-%m-%d"), messy.index[-1].strftime("%Y-%m-%d"))

week = messy.loc["2024-03-04":"2024-03-10"]
print(len(week), week.sum())

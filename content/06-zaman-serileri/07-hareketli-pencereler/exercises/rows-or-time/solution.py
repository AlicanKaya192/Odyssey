import pandas as pd

messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]
fixed = messy.sort_index().groupby(level=0).sum()

day = pd.Timestamp("2024-07-20")
print(fixed.rolling(7).sum().loc[day])

position = fixed.index.get_loc(day)
first = fixed.index[position - 6]
print((day - first).days + 1)

by_time = fixed.rolling("7D")
print(by_time.sum().loc[day], by_time.count().loc[day])

print(int((by_time.count() < 7).sum()))

import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

d1 = s.diff()
d7 = s.diff(7)

print(round(float(s.std()), 1), round(float(d1.std()), 1), round(float(d7.std()), 1))
print(int(s.isna().sum()), int(d1.isna().sum()), int(d7.isna().sum()))


def weekday_gap(x):
    by_day = x.groupby(x.index.dayofweek).mean()
    return round(float(by_day.max() - by_day.min()), 1)


print(weekday_gap(d1), weekday_gap(d7))

back = d1.cumsum() + s.iloc[0]
print(bool((back.iloc[1:] - s.iloc[1:]).abs().max() < 1e-9))

rebuilt = d7.iloc[-1] + s.iloc[-8]
print(int(rebuilt), int(s.iloc[-1]))

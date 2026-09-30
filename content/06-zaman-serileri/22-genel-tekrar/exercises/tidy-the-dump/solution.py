import numpy as np
import pandas as pd

raw = pd.read_csv("bike_raw.csv")
raw["date"] = pd.to_datetime(raw["date"], format="%d.%m.%Y")
print(len(raw), int(raw.duplicated().sum()))

s = raw.drop_duplicates().set_index("date").sort_index()["rentals"]
s = s.asfreq("D").astype(float)

gap = s.isna()
block = (~gap).cumsum()
print(int(gap.sum()), int(gap.groupby(block).sum().max()))

low = s.idxmin()
week = pd.Timedelta(days=7)
print(low.strftime("%Y-%m-%d"), int(s.loc[low]), int(s.loc[low - week]), int(s.loc[low + week]))

s.loc[low] = np.nan
fill = pd.concat([s.shift(7), s.shift(-7)], axis=1).mean(axis=1)
s = s.fillna(fill).round()

print(s.loc["2023-06-05":"2023-06-08"].astype(int).tolist())
print(len(s), int(s.isna().sum()), int(s.sum()))

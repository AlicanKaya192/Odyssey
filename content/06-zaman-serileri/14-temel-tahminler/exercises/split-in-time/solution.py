import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
s = s.loc[:"2024-12-03"]

train = s.iloc[:-28]
test = s.iloc[-28:]
print(len(train), len(test))
print(train.index[-1].date(), test.index[0].date())

h = len(test)
future = pd.date_range(train.index[-1] + pd.Timedelta(days=1), periods=h, freq="D")
print(future[0].date(), future[-1].date())
print(future.equals(test.index))

print(round(float(train.mean()), 1), round(float(test.mean()), 1))

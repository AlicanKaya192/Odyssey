import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
s = s.loc[:"2024-12-03"]

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")


def seasonal_naive(train, h, m):
    last = train.iloc[-m:].to_numpy()
    values = [last[i % m] for i in range(h)]
    future = pd.date_range(train.index[-1], periods=h + 1, freq=train.index.freq)[1:]
    return pd.Series(values, index=future)


daily = seasonal_naive(s, 10, 7)
print([int(v) for v in daily])
print(daily.index[0].date(), daily.index[-1].date())

train = p.loc[:"2023"]
monthly = seasonal_naive(train, 12, 12)
print([int(v) for v in monthly])

error = p.loc["2024"] - monthly
print(round(float(error.abs().mean()), 2), round(float(error.mean()), 2))

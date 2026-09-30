import pandas as pd

close = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
r = close.pct_change()

vol = r.rolling(20).std() * (252 ** 0.5) * 100
print(round(float(vol.mean()), 1))
print(vol.idxmax().strftime("%Y-%m-%d"), round(float(vol.max()), 1))
print(vol.idxmin().strftime("%Y-%m-%d"), round(float(vol.min()), 1))

ma100 = close.rolling(100).mean()
above = (close > ma100).loc["2024"]
print(int(above.sum()), len(above))

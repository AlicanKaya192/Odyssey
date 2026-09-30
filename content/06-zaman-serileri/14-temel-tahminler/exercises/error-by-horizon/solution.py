import pandas as pd

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

by_horizon = [float((k.shift(-h) - k).abs().mean()) for h in (1, 5, 10, 20, 40)]
print([round(v, 2) for v in by_horizon])
print(round(by_horizon[-1] / by_horizon[0], 1), round(40 ** 0.5, 1))

print([round(float((s - s.shift(7 * w)).abs().mean()), 1) for w in (1, 2, 4, 8)])
print([round(float((s - s.shift(h)).abs().mean()), 1) for h in (1, 3, 7)])

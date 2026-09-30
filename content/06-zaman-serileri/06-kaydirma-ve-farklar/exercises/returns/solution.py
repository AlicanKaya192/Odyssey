import numpy as np
import pandas as pd

close = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
r = close.pct_change()

print(round(float((close.iloc[-1] / close.iloc[0] - 1) * 100), 1))
print(round(float(r.sum() * 100), 1))
print(round(float(((1 + r).cumprod().iloc[-1] - 1) * 100), 1))

log_r = np.log(close).diff()
print(round(float((np.exp(log_r.sum()) - 1) * 100), 1))

print(r.idxmax().strftime("%Y-%m-%d"), round(float(r.max() * 100), 2))

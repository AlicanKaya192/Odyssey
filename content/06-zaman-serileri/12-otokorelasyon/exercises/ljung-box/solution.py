import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]


def memory(x, lags):
    table = acorr_ljungbox(x, lags=[lags])
    return round(float(table["lb_pvalue"].iloc[0]), 4)


change = k.diff().dropna()
cases = [("price", k, 10), ("price change", change, 10), ("sales d7", s.diff(7).dropna(), 14)]

for name, x, lags in cases:
    p = memory(x, lags)
    print(name, p, "memory" if p < 0.05 else "noise")

table = acorr_ljungbox(change, lags=[10])
print(round(float(table["lb_stat"].iloc[0]), 2))

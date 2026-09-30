import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]


def memory(x, lags):
    # The Ljung-Box p-value (four decimals).
    pass


# Three series: name, p, verdict (memory / noise).


# The test statistic for the daily difference of the price.

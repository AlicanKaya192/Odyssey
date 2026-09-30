import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]


def memory(x, lags):
    # Ljung-Box p-degeri (dort ondalik).
    pass


# Uc seri: ad, p, karar (memory / noise).


# Fiyatin gunluk farki icin test istatistigi.

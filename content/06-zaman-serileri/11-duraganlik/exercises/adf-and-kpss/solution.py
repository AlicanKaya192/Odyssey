import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]


def verdict(x):
    adf_p = float(adfuller(x)[1])
    kpss_p = float(kpss(x, regression="c", nlags="auto")[1])
    adf_ok = adf_p < 0.05
    kpss_ok = kpss_p >= 0.05
    if adf_ok and kpss_ok:
        text = "stationary"
    elif not adf_ok and not kpss_ok:
        text = "not stationary"
    else:
        text = "mixed"
    return round(adf_p, 3), round(kpss_p, 3), text


print(verdict(k))
print(verdict(k.diff().dropna()))

result = adfuller(k)
print(round(float(result[0]), 2), round(float(result[4]["5%"]), 2))

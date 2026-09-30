import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

w = pd.read_csv("two_processes.csv", index_col="date", parse_dates=True).asfreq("D")

fits = {}
for name in ("x", "y"):
    ar = ARIMA(w[name], order=(1, 0, 0)).fit()
    ma = ARIMA(w[name], order=(0, 0, 1)).fit()
    fits[name] = (ar, ma)
    print(name, round(float(ar.aic), 1), round(float(ma.aic), 1))

for name, (ar, ma) in fits.items():
    if ar.aic < ma.aic:
        print(name, "AR", round(float(ar.params["ar.L1"]), 2))
    else:
        print(name, "MA", round(float(ma.params["ma.L1"]), 2))

big = ARIMA(w["x"], order=(2, 0, 0)).fit()
print(round(float(big.params["ar.L2"]), 2), round(float(big.pvalues["ar.L2"]), 2))
print(round(float(fits["x"][0].aic), 1), round(float(big.aic), 1))

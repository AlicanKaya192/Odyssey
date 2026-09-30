import warnings

warnings.simplefilter("ignore")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

train, test = p.loc[:"2023"], p.loc["2024"]

fit = ARIMA(np.log(train), order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()
print(round(float(fit.params["ma.L1"]), 2), round(float(fit.params["ma.S.L12"]), 2))

forecast = np.exp(fit.forecast(12))
error = (test - forecast).abs()
print(round(float(error.mean()), 2), round(float((error / test).mean() * 100), 1))

plain = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12)).fit()
print(round(float((test - plain.forecast(12)).abs().mean()), 2))

check = acorr_ljungbox(fit.resid.iloc[13:], lags=[12])
print(round(float(check["lb_pvalue"].iloc[0]), 2))

month = "2024-08-01"
print(round(float(forecast.loc[month])), int(test.loc[month]))

recent = p.loc["2022":]
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(recent.index, recent.values, color="gray", label="actual")
ax.plot(forecast.index, forecast.values, linewidth=2, label="forecast")
ax.legend()
fig.savefig("chart.png")

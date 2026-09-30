import warnings

warnings.simplefilter("ignore")

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]
test = s.loc["2024-11-06":"2024-12-03"]

fit = ExponentialSmoothing(train, seasonal="add", seasonal_periods=7).fit()

print(round(float(fit.params["smoothing_level"]), 2),
      round(float(fit.params["smoothing_seasonal"]), 2))
print(round(float(fit.level.iloc[-1]), 1))
print([round(float(v), 1) for v in fit.season.iloc[-7:]])

forecast = fit.forecast(28)
print([round(float(v), 1) for v in forecast.iloc[:7]])

error = test - forecast
print(round(float(error.abs().mean()), 2), round(float(error.mean()), 2))

recent = s.loc["2024-10-09":"2024-12-03"]
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(recent.index, recent.values, color="gray", label="actual")
ax.plot(forecast.index, forecast.values, linewidth=2, label="forecast")
ax.legend()
fig.savefig("chart.png")

import warnings

warnings.simplefilter("ignore")

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]
test = s.loc["2024-11-06":"2024-12-03"]
fit = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 7)).fit()

result = fit.get_forecast(28)
mean = result.predicted_mean
wide = result.conf_int(alpha=0.05)
low, high = wide.iloc[:, 0], wide.iloc[:, 1]

print(round(float(mean.iloc[0]), 1), round(float(low.iloc[0]), 1),
      round(float(high.iloc[0]), 1), int(test.iloc[0]))

width = high - low
print([round(float(width.iloc[i]), 1) for i in (0, 6, 13, 27)])

narrow = result.conf_int(alpha=0.2)
inside_95 = (test >= low) & (test <= high)
inside_80 = (test >= narrow.iloc[:, 0]) & (test <= narrow.iloc[:, 1])
print(round(float(inside_95.mean()), 3), round(float(inside_80.mean()), 3))

print(test.index[~inside_95].strftime("%m-%d").tolist())

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(test.index, test.values, color="gray", label="actual")
ax.plot(mean.index, mean.values, label="forecast")
ax.fill_between(mean.index, low.values, high.values, alpha=0.2, label="95%")
ax.legend()
fig.savefig("chart.png")

import warnings

warnings.simplefilter("ignore")

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")

train = c.loc[:"2024-10-31"]
test = c.loc["2024-11-01":"2024-11-28"]
columns = ["promo", "holiday", "temp_c"]

fit = ARIMA(train["sales"], exog=train[columns], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()
with_exog = fit.forecast(28, exog=test[columns])

plain = ARIMA(train["sales"], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()
without = plain.forecast(28)

actual = test["sales"]
print(round(float((actual - without).abs().mean()), 2), round(float((actual - with_exog).abs().mean()), 2))

promo_days = test.index[test["promo"] == 1]
print(promo_days.strftime("%m-%d").tolist())

for day in promo_days:
    print(int(actual.loc[day]), round(float(without.loc[day])), round(float(with_exog.loc[day])))

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(actual.index, actual.values, color="gray", label="actual")
ax.plot(without.index, without.values, label="without")
ax.plot(with_exog.index, with_exog.values, label="with exog")
ax.legend()
fig.savefig("chart.png")

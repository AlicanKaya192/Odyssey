import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")

train = c.loc[:"2024-10-31"]
test = c.loc["2024-11-01":"2024-11-28"]
columns = ["promo", "holiday", "temp_c"]

fit = ARIMA(train["sales"], exog=train[columns], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()

normal = train["temp_c"].groupby(train.index.dayofyear).mean()

futures = {}
futures["actual"] = test[columns].copy()

futures["last"] = test[columns].copy()
futures["last"]["temp_c"] = train["temp_c"].iloc[-1]

futures["normal"] = test[columns].copy()
futures["normal"]["temp_c"] = [normal[day] for day in test.index.dayofyear]

for name, future in futures.items():
    print(name, round(float((test["temp_c"] - future["temp_c"]).abs().mean()), 1))

scores = {}
for name, future in futures.items():
    forecast = fit.forecast(28, exog=future)
    scores[name] = float((test["sales"] - forecast).abs().mean())
    print(name, round(scores[name], 2))

honest = min(scores["last"], scores["normal"])
print(round(honest - scores["actual"], 2))

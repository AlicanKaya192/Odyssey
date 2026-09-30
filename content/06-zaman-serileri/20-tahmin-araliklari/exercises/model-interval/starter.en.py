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

# get_forecast(28): the forecast and the 95% interval.


# The first day: forecast, lower end, upper end, actual.


# Width of the interval on days 1, 7, 14, 28.


# Coverage: 95% and 80%.


# The days outside the 95% interval.


# Chart: actual, forecast, the band with fill_between; chart.png.

import warnings

warnings.simplefilter("ignore")

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")

train = c.loc[:"2024-10-31"]
test = c.loc["2024-11-01":"2024-11-28"]
columns = ["promo", "holiday", "temp_c"]

# The model with external variables and its 28-day forecast.


# The model without external variables and its 28-day forecast.


# MAE of the two forecasts (the one without first).


# The campaign days in the test period.


# On those days: actual, forecast without, forecast with.


# Chart: chart.png.

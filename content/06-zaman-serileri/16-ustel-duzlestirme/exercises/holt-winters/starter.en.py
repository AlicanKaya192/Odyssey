import warnings

warnings.simplefilter("ignore")

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]
test = s.loc["2024-11-06":"2024-12-03"]

# The model with no trend and an additive season.


# alpha and gamma.


# The last level.


# The last 7 seasonal shares.


# The 28-day forecast; its first 7 days.


# MAE and bias.


# Chart: chart.png.

import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]
test = s.loc["2024-11-06":"2024-12-03"]

candidates = [
    ((0, 0, 0), (0, 1, 0, 7)),
    ((1, 0, 0), (0, 1, 1, 7)),
    ((0, 1, 1), (0, 1, 1, 7)),
    ((1, 1, 1), (0, 1, 1, 7)),
]

# Each candidate: AIC, Ljung-Box p-value, MAE; print a line.


# The order of the candidate with the smallest AIC.


# The candidates whose Ljung-Box p-value is above 0.05.

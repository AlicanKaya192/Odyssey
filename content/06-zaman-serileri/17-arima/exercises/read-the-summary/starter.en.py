import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]

# The (1,1,1)(0,1,1,7) model.


# The coefficients except sigma2: name, value, p-value.


# The coefficients with a p-value above 0.05.


# The (0,1,1)(0,1,1,7) model; the AIC of the two models.


# The residual standard deviation of the two models.

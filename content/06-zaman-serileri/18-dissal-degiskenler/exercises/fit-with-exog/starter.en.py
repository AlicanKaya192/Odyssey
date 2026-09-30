import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")

train = c.loc[:"2024-10-31"]
columns = ["promo", "holiday", "temp_c"]

# The model without external variables.


# The model with external variables.


# The AIC of the two models.


# The coefficients of the three external variables.


# The confidence intervals of the three coefficients (lower, upper).


# The residual standard deviation of the two models.

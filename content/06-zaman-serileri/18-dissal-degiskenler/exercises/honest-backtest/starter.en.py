import warnings

warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")
cuts = [pd.Timestamp("2024-01-30") + pd.Timedelta(days=56 * i) for i in range(6)]


def plain(train, test):
    fit = ARIMA(train["sales"], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()
    return fit.forecast(28).to_numpy()


def with_exog(train, test):
    # The model with exog; in the future table temp_c = the seasonal normal from training.
    pass


# Two methods, 6 experiments: the MAE of each experiment.


# Each method: name, mean MAE, worst experiment.


# Wins and skill of the model with external variables.

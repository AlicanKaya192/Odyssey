import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf

# Read the file with a date index.


# x: ACF and PACF, first 4 lags (two lines).


# y: ACF and PACF, first 4 lags (two lines).


def kind(series):
    # "MA" if the ACF at lag 2 is inside the band, otherwise "AR".
    pass


# kind(x) and kind(y).

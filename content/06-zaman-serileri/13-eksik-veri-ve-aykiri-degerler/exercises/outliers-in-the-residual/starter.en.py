import pandas as pd
from statsmodels.tsa.seasonal import STL

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]


def robust(x):
    median = x.median()
    mad = (x - median).abs().median()
    return 0.6745 * (x - median) / mad


# The interquartile range rule on the raw series: number of flagged days.


# How many of them are after 2 September.


# Robust STL, the robust score of the residual.


# The 5 days with the largest score, and their scores.


# Number of days with |score| > 3.5 and with |score| > 20.

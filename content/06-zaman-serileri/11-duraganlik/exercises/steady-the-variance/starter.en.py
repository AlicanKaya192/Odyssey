import numpy as np
import pandas as pd

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"]
periods = [("2013", "2016"), ("2017", "2020"), ("2021", "2024")]

# Std of the plain difference in the three periods (one decimal, a list).


# Std of the log difference in the three periods (three decimals, a list).


# Last period / first period ratio: plain difference, log difference.


# Yearly growth rate (percent, one decimal).


# First defined date of growth and its NaN count.

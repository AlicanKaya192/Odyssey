import matplotlib.pyplot as plt
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# 7- and 28-day means on the whole series, then select 2024.


# Three lines: daily (faint), 7-day mean, 28-day mean.


# Legend and save.


# Number of lines.


# Legend labels (a list).


# NaN counts within 2024: 7-day and 28-day.

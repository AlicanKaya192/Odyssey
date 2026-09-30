import matplotlib.pyplot as plt
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Mean by day of the week.


# Bar chart and save.


# Number of bars.


# Lower limit of the vertical axis.


# The highest and the lowest day: name and mean.


# Weekend / weekday ratio (two decimals).

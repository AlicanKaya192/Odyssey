import pandas as pd

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

train, test = p.loc[:"2023"], p.loc["2024"]

# base: the twelve values of 2023.


# Drift: add slope * 12 to every month.


# Growth: print the rate, multiply every month by it.


# Three forecasts: name, MAE, percentage error.


# Skill of the growth forecast over seasonal naive.


# August 2024: actual and the three forecasts.

import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
past = pd.concat([v.shift(7 * k) for k in (1, 2, 3, 4)], axis=1)


def alarms(expected):
    # Days whose relative deviation passes 0.25 (a "%m-%d" list).
    pass


# With the median: number of alarms and the list.


# With the mean: number of alarms.


# Days that alarm with the mean but not with the median.


# 21 March: mean expectation, median expectation, actual.

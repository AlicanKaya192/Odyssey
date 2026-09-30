import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
past = pd.concat([v.shift(7 * k) for k in (1, 2, 3, 4)], axis=1)
deviation = v / past.median(axis=1) - 1
alarm = deviation.abs() > 0.25

# The alarm days.


# Split the days into events (a gap of at most 3 days).


# Each event: first day, last day, number of alarms, direction, kind.

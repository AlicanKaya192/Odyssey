import pandas as pd

p = pd.read_csv("pump_pressure.csv", index_col="timestamp", parse_dates=True)
p = p["pressure"]
events = pd.read_csv("pump_events.csv", parse_dates=["timestamp"])["timestamp"]
calm = p.loc[:"2024-10-06"]

# z-score over the whole series: hours past 3 and how many are in events.


# 03:00 on 5 September: value, z-score, the median of that hour.


# Hour profile, residual, robust score.


# Number of hours with a score past 3 and how many are in events.


# Days of the hours that are flagged but not in events.

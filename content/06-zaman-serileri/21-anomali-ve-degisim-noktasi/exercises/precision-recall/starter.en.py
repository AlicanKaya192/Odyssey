import pandas as pd

p = pd.read_csv("pump_pressure.csv", index_col="timestamp", parse_dates=True)
p = p["pressure"]
events = pd.read_csv("pump_events.csv", parse_dates=["timestamp"])["timestamp"]
calm = p.loc[:"2024-10-06"]

profile = calm.groupby(calm.index.hour).median()
resid = calm - profile.reindex(calm.index.hour).to_numpy()
mad = (resid - resid.median()).abs().median()
score = 0.6745 * (resid - resid.median()) / mad


def evaluate(threshold, skip):
    # Number of alarms, number correct, precision, recall.
    pass


# Threshold 3, nothing skipped.


# Stuck-sensor hours set aside: thresholds 2, 2.5, 3, 4, 6.


# The events missed at a threshold of 4.

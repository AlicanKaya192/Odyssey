import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
ref = v.loc["2024-01":"2024-02"]
profile = ref.groupby(ref.index.dayofweek).median()
rel = v / profile.reindex(v.index.dayofweek).to_numpy() - 1
sd = (ref / profile.reindex(ref.index.dayofweek).to_numpy() - 1).std()
z = rel / sd


def cusum(z, k, h):
    # Accumulate the sum; past h, add the day to the list and reset the sum.
    pass


# Clipped series, k = 1, h = 8: first alarm, days after 2 September, number of alarms.


# Unclipped series: first alarm.


# Clipped series, k = 0.5, h = 5: the alarms before 2 September.

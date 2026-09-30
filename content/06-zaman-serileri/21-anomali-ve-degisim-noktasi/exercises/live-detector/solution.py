import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
past = pd.concat([v.shift(7 * k) for k in (1, 2, 3, 4)], axis=1)


def alarms(expected):
    deviation = v / expected - 1
    return deviation[deviation.abs() > 0.25].index.strftime("%m-%d").tolist()


by_median = alarms(past.median(axis=1))
print(len(by_median))
print(by_median)

by_mean = alarms(past.mean(axis=1))
print(len(by_mean))

print([day for day in by_mean if day not in by_median])

day = "2024-03-21"
print(round(float(past.mean(axis=1).loc[day])), round(float(past.median(axis=1).loc[day])),
      int(v.loc[day]))

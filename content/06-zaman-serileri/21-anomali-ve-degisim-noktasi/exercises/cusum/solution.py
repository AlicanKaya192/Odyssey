import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
ref = v.loc["2024-01":"2024-02"]
profile = ref.groupby(ref.index.dayofweek).median()
rel = v / profile.reindex(v.index.dayofweek).to_numpy() - 1
sd = (ref / profile.reindex(ref.index.dayofweek).to_numpy() - 1).std()
z = rel / sd


def cusum(z, k, h):
    total = 0.0
    alarms = []
    for day, value in z.items():
        total = max(0.0, total + value - k)
        if total > h:
            alarms.append(day)
            total = 0.0
    return alarms


change = pd.Timestamp("2024-09-02")
clipped = z.clip(-3, 3)

found = cusum(clipped, 1.0, 8.0)
print(found[0].strftime("%Y-%m-%d"), (found[0] - change).days, len(found))

print(cusum(z, 1.0, 8.0)[0].strftime("%Y-%m-%d"))

early = [day for day in cusum(clipped, 0.5, 5.0) if day < change]
print([day.strftime("%m-%d") for day in early])

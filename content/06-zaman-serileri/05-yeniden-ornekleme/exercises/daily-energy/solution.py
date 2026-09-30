import pandas as pd

load = pd.read_csv("energy_hourly.csv", index_col="timestamp", parse_dates=True)["load_mw"]

total = load.resample("D").sum()
peak = load.resample("D").max()

print(len(total))
print(total.idxmax().strftime("%Y-%m-%d"), round(float(total.max()), 1))
print(peak.idxmax().strftime("%Y-%m-%d"), peak.max())

weekend = total.index.dayofweek >= 5
print(round(float(total[~weekend].mean())), round(float(total[weekend].mean())))

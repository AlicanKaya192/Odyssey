import pandas as pd

load = pd.read_csv("energy_hourly.csv", index_col="timestamp", parse_dates=True)["load_mw"]

print(len(load.loc["2024-03-15"]))

day = load.between_time("08:00", "18:00").mean()
night = load.between_time("22:00", "06:00").mean()
print(round(float(day), 1), round(float(night), 1))
print(round(float(day / night), 2))

print(round(float(load.at_time("18:00").mean()), 1))

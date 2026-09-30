import pandas as pd

temp = pd.read_csv("machine_log.csv", index_col="time", parse_dates=True)["temp_c"]

print(temp.index.to_series().diff().max())

hourly = temp.resample("h").mean()
empty = hourly.isna()
print(len(hourly), int(empty.sum()))
print(hourly.index[empty].strftime("%m-%d %H:%M").tolist())

print(temp.resample("h").sum().loc["2024-05-07 04:00"], hourly.loc["2024-05-07 04:00"])

filled = hourly.interpolate()
print(round(float(filled.loc["2024-05-07 05:00"]), 2))

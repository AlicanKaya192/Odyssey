import pandas as pd

sensor = pd.read_csv("berlin_sensor.csv")
sensor["time_utc"] = pd.to_datetime(sensor["time_utc"])
sensor["local"] = sensor["time_utc"].dt.tz_convert("Europe/Berlin")

counts = sensor["local"].dt.date.value_counts().sort_index()
for day, count in counts.items():
    print(day, count)

hottest = sensor.loc[sensor["temp_c"].idxmax(), "local"]
print(hottest.strftime("%Y-%m-%d %H:%M"))

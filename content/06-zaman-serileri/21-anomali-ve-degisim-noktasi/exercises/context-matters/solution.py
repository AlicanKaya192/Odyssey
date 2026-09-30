import pandas as pd

p = pd.read_csv("pump_pressure.csv", index_col="timestamp", parse_dates=True)
p = p["pressure"]
events = pd.read_csv("pump_events.csv", parse_dates=["timestamp"])["timestamp"]
calm = p.loc[:"2024-10-06"]

z = (calm - calm.mean()) / calm.std()
found = z[z.abs() > 3].index
print(found.strftime("%m-%d %H").tolist(), int(found.isin(events).sum()))

moment = pd.Timestamp("2024-09-05 03:00")
profile = calm.groupby(calm.index.hour).median()
print(float(calm.loc[moment]), round(float(z.loc[moment]), 1), float(profile.loc[3]))

resid = calm - profile.reindex(calm.index.hour).to_numpy()
mad = (resid - resid.median()).abs().median()
score = 0.6745 * (resid - resid.median()) / mad

flagged = score[score.abs() > 3].index
print(len(flagged), int(flagged.isin(events).sum()))

other = flagged[~flagged.isin(events)]
print(sorted(set(other.strftime("%m-%d"))))

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
    kept = score.drop(skip)
    flagged = kept[kept.abs() > threshold].index
    correct = int(flagged.isin(events).sum())
    return len(flagged), correct, round(correct / len(flagged), 2), round(correct / len(events), 2)


print(evaluate(3, []))

stuck = pd.date_range("2024-09-30 08:00", "2024-09-30 16:00", freq="h")
for threshold in (2, 2.5, 3, 4, 6):
    print(threshold, evaluate(threshold, stuck))

caught = score[score.abs() > 4].index
missed = events[~events.isin(caught)]
print(missed.dt.strftime("%m-%d %H").tolist())

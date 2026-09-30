import pandas as pd

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]
days = pd.to_datetime(["2024-03-14", "2024-06-20", "2024-10-08"])

clean = visits.astype(float).copy()
clean.loc[days] = float("nan")

both = pd.concat([clean.shift(7), clean.shift(-7)], axis=1).mean(axis=1)
clean = clean.fillna(both)
print(clean.loc[days].tolist())

table = pd.DataFrame({
    "visits": visits,
    "clean": clean,
    "repaired": visits.index.isin(days),
})
print(len(table), int(table["repaired"].sum()))

print(round(float(table["visits"].std()), 1), round(float(table["clean"].std()), 1))

thursday = table[table.index.dayofweek == 3]
print(round(float(thursday["visits"].mean()), 1), round(float(thursday["clean"].mean()), 1))

campaigns = days[:2]
effect = (table.loc[campaigns, "visits"] - table.loc[campaigns, "clean"]).sum()
print(int(effect))

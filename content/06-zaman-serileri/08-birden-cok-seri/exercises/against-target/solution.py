import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])
targets = pd.read_csv("targets.csv")

long["month"] = long["date"].dt.to_period("M").astype(str)
actual = long.groupby(["month", "store"])["sales"].sum().reset_index()

report = actual.merge(targets, on=["month", "store"], how="left")
report["pct"] = (report["sales"] / report["target"] * 100).round(1)

june = report[report["month"] == "2024-06"]
for store, pct in zip(june["store"], june["pct"]):
    print(store, pct)

print(int((report["pct"] >= 100).sum()), len(report))

worst = report.loc[report["pct"].idxmin()]
print(worst["month"], worst["store"], worst["pct"])

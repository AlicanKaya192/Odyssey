import pandas as pd

raw = pd.read_csv("sales_messy.csv", parse_dates=["date"])
full = raw.groupby("date")["sales"].sum().sort_index().asfreq("D")
truth = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

days = full[full.isna()].index


def score(filled):
    return round(float((filled.loc[days] - truth.loc[days]).abs().mean()), 1)


both = pd.concat([full.shift(7), full.shift(-7)], axis=1).mean(axis=1)
methods = {
    "ffill": full.ffill(),
    "linear": full.interpolate(),
    "week ago": full.fillna(full.shift(7)),
    "both sides": full.fillna(both),
}

for name, filled in methods.items():
    print(name, score(filled))

day = "2024-02-10"
print(int(truth.loc[day]), *[round(float(filled.loc[day])) for filled in methods.values()])

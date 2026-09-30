import pandas as pd

raw = pd.read_csv("sales_messy.csv", parse_dates=["date"])
print(len(raw), raw["date"].nunique(), int(raw["sales"].isna().sum()))

twice = raw.loc[raw["date"].duplicated(), "date"].sort_values()
print(twice.dt.strftime("%m-%d").tolist())

full = raw.groupby("date")["sales"].sum().sort_index().asfreq("D")
print(len(full), int(full.isna().sum()))

missing = full.isna()
print(full[missing].index.strftime("%m-%d").tolist())

run_id = (missing != missing.shift()).cumsum()
lengths = missing.groupby(run_id).sum()
print([int(v) for v in lengths[lengths > 0]])

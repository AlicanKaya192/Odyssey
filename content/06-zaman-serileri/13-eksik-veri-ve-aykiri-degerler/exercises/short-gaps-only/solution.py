import pandas as pd

x = pd.read_csv("machine_log.csv", index_col="time", parse_dates=True)["temp_c"]
r = x.resample("10min").mean()
print(len(r), int(r.isna().sum()))

missing = r.isna()
run_id = (missing != missing.shift()).cumsum()
lengths = missing.groupby(run_id).sum()
lengths = lengths[lengths > 0]
print(len(lengths), int(lengths.max()), int(lengths[lengths <= 3].sum()))

run_length = missing.groupby(run_id).transform("sum")
short = missing & (run_length <= 3)
result = r.where(~short, r.interpolate())
print(int(result.isna().sum()))

print(int(r.interpolate(limit=3).isna().sum()))

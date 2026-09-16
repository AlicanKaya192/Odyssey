import pandas as pd

raw = pd.read_csv("results_raw.csv")

data = raw.copy()
data["city"] = data["city"].str.strip().str.title()
data["score"] = pd.to_numeric(data["score"], errors="coerce")

start = len(data)
data = data.drop_duplicates(subset=["id"])
unique_rows = len(data)
missing = int(data["score"].isna().sum())
data = data.dropna(subset=["score"])

print(start, unique_rows, missing, len(data))
summary = data.groupby("city")["score"].agg(["count", "mean"])
print(summary["count"].to_dict())
print(summary["mean"].round(1).to_dict())

import pandas as pd

raw = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 5, 6],
    "city": ["Ankara", "Izmir ", "ankara", "Bursa", "Izmir", "Izmir", "ANKARA"],
    "score": ["82", "74", "91", None, "68", "68", "abc"],
})

data = raw.copy()
data["city"] = data["city"].str.strip().str.title()
data["score"] = pd.to_numeric(data["score"], errors="coerce")

start = len(data)
data = data.drop_duplicates(subset=["id"])
unique_rows = len(data)
missing = int(data["score"].isna().sum())
data = data.dropna(subset=["score"])

print(start, unique_rows, missing, len(data))
print(data.groupby("city")["score"].agg(["count", "mean"]))

import pandas as pd

raw = pd.DataFrame({
    "Name ": [" Ada", "Kerem", "Mina ", "Deniz", "Efe", "Sila"],
    "City ": ["ankara", "Izmir ", "ANKARA", " bursa", "izmir", "Ankara "],
    "score": ["82", "74", "91", "68", "88", "76"],
})

data = raw.copy()
data.columns = data.columns.str.strip().str.lower()
data["name"] = data["name"].str.strip()
data["city"] = data["city"].str.strip().str.title()
data["score"] = pd.to_numeric(data["score"], errors="coerce")

print(data.columns.tolist())
print(data.dtypes.astype(str).tolist())
print(data["city"].value_counts().to_dict())
print(round(data["score"].mean(), 2))

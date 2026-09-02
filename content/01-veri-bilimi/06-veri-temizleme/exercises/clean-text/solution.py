import pandas as pd

raw = pd.DataFrame({
    " Name ": [" Ada ", "kerem", "MINA", "Ada ", "Deniz", "efe ", "Sila"],
    "city": ["Ankara", "izmir ", "ANKARA", "Ankara", "bursa", "IZMIR", "Ankara "],
    "score": ["82", "74", "91", "82", "abc", "88", "-1"],
})

data = raw.copy()
data.columns = data.columns.str.strip().str.lower()

print(int(data["city"].nunique()))

data["name"] = data["name"].str.strip().str.title()
data["city"] = data["city"].str.strip().str.title()

print(data[["name", "city"]])
print(int(data["city"].nunique()))

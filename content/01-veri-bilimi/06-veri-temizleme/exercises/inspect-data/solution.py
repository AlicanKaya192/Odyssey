import pandas as pd

raw = pd.DataFrame({
    " Name ": [" Ada ", "kerem", "MINA", "Ada ", "Deniz", "efe ", "Sila"],
    "city": ["Ankara", "izmir ", "ANKARA", "Ankara", "bursa", "IZMIR", "Ankara "],
    "score": ["82", "74", "91", "82", "abc", "88", "-1"],
})

print(raw.shape)
print(list(raw.columns))
print(raw.dtypes.astype(str).tolist())
print(int(raw.isna().sum().sum()))
print(int(raw.duplicated().sum()))

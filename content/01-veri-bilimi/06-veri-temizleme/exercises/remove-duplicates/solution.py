import pandas as pd

raw = pd.DataFrame({
    " Name ": [" Ada ", "kerem", "MINA", "Ada ", "Deniz", "efe ", "Sila"],
    "city": ["Ankara", "izmir ", "ANKARA", "Ankara", "bursa", "IZMIR", "Ankara "],
    "score": ["82", "74", "91", "82", "abc", "88", "-1"],
})

import numpy as np

data = raw.copy()
data.columns = data.columns.str.strip().str.lower()
data["name"] = data["name"].str.strip().str.title()
data["city"] = data["city"].str.strip().str.title()
data["score"] = pd.to_numeric(data["score"], errors="coerce").replace(-1, np.nan)

print(int(data.duplicated(subset=["name"]).sum()))

clean = data.drop_duplicates(subset=["name"])
clean = clean.dropna(subset=["score"]).reset_index(drop=True)

print(clean.shape)
print(clean)
print(round(clean["score"].mean(), 2))

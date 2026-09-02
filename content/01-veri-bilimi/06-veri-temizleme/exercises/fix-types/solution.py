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

data["score"] = pd.to_numeric(data["score"], errors="coerce")
data["score"] = data["score"].replace(-1, np.nan)

print(data["score"].tolist())
print(str(data["score"].dtype))
print(int(data["score"].isna().sum()))

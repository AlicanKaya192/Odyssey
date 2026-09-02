import pandas as pd

raw = pd.DataFrame({
    " Name ": [" Ada ", "kerem", "MINA", "Ada ", "Deniz", "efe ", "Sila"],
    "city": ["Ankara", "izmir ", "ANKARA", "Ankara", "bursa", "IZMIR", "Ankara "],
    "score": ["82", "74", "91", "82", "abc", "88", "-1"],
})

data = raw.copy()
data.columns = data.columns.str.strip().str.lower()
data["name"] = data["name"].str.strip().str.title()
data["city"] = data["city"].str.strip().str.title()

# Convert the score column to numeric; unconvertible values stay empty.


# Turn the value -1 into a real missing value.


# Print the column's values as a list.


# Print the column's type.


# Print how many values are missing.

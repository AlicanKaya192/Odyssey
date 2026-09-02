import pandas as pd

raw = pd.DataFrame({
    " Name ": [" Ada ", "kerem", "MINA", "Ada ", "Deniz", "efe ", "Sila"],
    "city": ["Ankara", "izmir ", "ANKARA", "Ankara", "bursa", "IZMIR", "Ankara "],
    "score": ["82", "74", "91", "82", "abc", "88", "-1"],
})

data = raw.copy()
data.columns = data.columns.str.strip().str.lower()

# Print how many distinct cities there are before cleaning.


# Strip the spaces in name and city, and capitalise the first letters.


# Print the name and city columns.


# Print how many distinct cities there are after cleaning.

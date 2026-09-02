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

# score sutununu sayiya cevir; cevrilemeyenler bos kalsin.


# -1 degerini gercek bir eksik degere cevir.


# Sutunun degerlerini liste halinde yazdir.


# Sutunun tipini yazdir.


# Kac eksik deger oldugunu yazdir.

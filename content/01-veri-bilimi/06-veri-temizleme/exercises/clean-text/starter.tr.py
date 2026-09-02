import pandas as pd

raw = pd.DataFrame({
    " Name ": [" Ada ", "kerem", "MINA", "Ada ", "Deniz", "efe ", "Sila"],
    "city": ["Ankara", "izmir ", "ANKARA", "Ankara", "bursa", "IZMIR", "Ankara "],
    "score": ["82", "74", "91", "82", "abc", "88", "-1"],
})

data = raw.copy()
data.columns = data.columns.str.strip().str.lower()

# Temizlemeden once kac farkli sehir oldugunu yazdir.


# name ve city sutunlarindaki bosluklari at, ilk harfleri buyut.


# name ve city sutunlarini yazdir.


# Temizledikten sonra kac farkli sehir oldugunu yazdir.

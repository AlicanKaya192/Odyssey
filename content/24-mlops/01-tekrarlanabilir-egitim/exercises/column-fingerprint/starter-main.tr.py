import hashlib
import json
from ml_data import make_customers, FEATURES


def fingerprint(rows, columns):
    # Yalnizca istenen sutunlari tut, metne cevir, ozetin ilk 12 karakterini dondur.
    pass


rows = make_customers(200)
print("features:", fingerprint(rows, FEATURES))
for row in rows:
    row["id"] = "X" + row["id"]
print("new ids:", fingerprint(rows, FEATURES))
rows[0]["tenure"] = rows[0]["tenure"] + 1
print("one change:", fingerprint(rows, FEATURES))

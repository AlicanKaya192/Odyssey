import hashlib
import json
from ml_data import make_customers, FEATURES


def fingerprint(rows, columns):
    # Keep only the requested columns, turn them into text, return the first 12 characters of the hash.
    pass


rows = make_customers(200)
print("features:", fingerprint(rows, FEATURES))
for row in rows:
    row["id"] = "X" + row["id"]
print("new ids:", fingerprint(rows, FEATURES))
rows[0]["tenure"] = rows[0]["tenure"] + 1
print("one change:", fingerprint(rows, FEATURES))

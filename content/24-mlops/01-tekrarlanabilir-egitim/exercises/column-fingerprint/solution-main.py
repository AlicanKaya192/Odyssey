import hashlib
import json
from ml_data import make_customers, FEATURES


def fingerprint(rows, columns):
    kept = [{c: row[c] for c in columns} for row in rows]
    text = json.dumps(kept, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


rows = make_customers(200)
print("features:", fingerprint(rows, FEATURES))
for row in rows:
    row["id"] = "X" + row["id"]
print("new ids:", fingerprint(rows, FEATURES))
rows[0]["tenure"] = rows[0]["tenure"] + 1
print("one change:", fingerprint(rows, FEATURES))

from rules import SCHEMA, check_row
from ml_data import make_customers


def gate(rows, schema, max_bad_share):
    if not rows:
        return {"status": "rejected", "good": 0, "quarantined": 0}
    good = 0
    quarantined = 0
    for row in rows:
        if check_row(row, schema):
            quarantined += 1
        else:
            good += 1
    status = "rejected" if quarantined / len(rows) > max_bad_share else "accepted"
    return {"status": status, "good": good, "quarantined": quarantined}


batch = make_customers(200, seed=5)
result = gate(batch, SCHEMA, 0.05)
print(result["status"], result["good"], result["quarantined"])
for row in batch[:12]:
    row["plan"] = "PRO"
result = gate(batch, SCHEMA, 0.05)
print(result["status"], result["good"], result["quarantined"])
result = gate([], SCHEMA, 0.05)
print(result["status"], result["good"], result["quarantined"])

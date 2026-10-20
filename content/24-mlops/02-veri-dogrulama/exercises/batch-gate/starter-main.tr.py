from rules import SCHEMA, check_row
from ml_data import make_customers


def gate(rows, schema, max_bad_share):
    # Bos partiyi reddet, satirlari say, payi sinirla karsilastir.
    pass


batch = make_customers(200, seed=5)
result = gate(batch, SCHEMA, 0.05)
print(result["status"], result["good"], result["quarantined"])
for row in batch[:12]:
    row["plan"] = "PRO"
result = gate(batch, SCHEMA, 0.05)
print(result["status"], result["good"], result["quarantined"])
result = gate([], SCHEMA, 0.05)
print(result["status"], result["good"], result["quarantined"])

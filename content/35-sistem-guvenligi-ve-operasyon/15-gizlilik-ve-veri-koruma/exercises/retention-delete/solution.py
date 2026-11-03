from datetime import date


def to_delete(records, retention, today):
    now = date.fromisoformat(today)
    found = []
    for rid, purpose, created in records:
        age = (now - date.fromisoformat(created)).days
        if purpose not in retention or age > retention[purpose]:
            found.append(rid)
    return sorted(found)

RECORDS = [
    ["r1", "marketing", "2025-06-01"],
    ["r2", "invoice", "2019-02-01"],
    ["r3", "support", "2025-01-10"],
    ["r4", "marketing", "2026-03-03"],
    ["r5", "survey", "2026-10-01"],
]
RETENTION = {"marketing": 365, "invoice": 3650, "support": 730}
print(to_delete(RECORDS, RETENTION, "2026-11-01"))

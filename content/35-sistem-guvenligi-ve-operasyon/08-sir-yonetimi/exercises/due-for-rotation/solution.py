from datetime import date


def due_for_rotation(secrets, today, max_days):
    now = date.fromisoformat(today)
    due = []
    for name, created in secrets:
        age = (now - date.fromisoformat(created)).days
        if age > max_days:
            due.append(name)
    return sorted(due)

SECRETS = [
    ["db-password", "2026-09-20"],
    ["api-token", "2026-06-01"],
    ["signing-key", "2025-12-15"],
    ["cache-key", "2026-08-03"],
]
print(due_for_rotation(SECRETS, "2026-11-01", 90))

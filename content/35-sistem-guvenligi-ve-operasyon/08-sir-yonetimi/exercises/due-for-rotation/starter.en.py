from datetime import date


def due_for_rotation(secrets, today, max_days):
    due = []
    # age = (today - created).days
    return due

SECRETS = [
    ["db-password", "2026-09-20"],
    ["api-token", "2026-06-01"],
    ["signing-key", "2025-12-15"],
    ["cache-key", "2026-08-03"],
]
print(due_for_rotation(SECRETS, "2026-11-01", 90))

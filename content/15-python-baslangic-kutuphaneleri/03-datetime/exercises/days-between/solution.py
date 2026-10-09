from datetime import date


def days_between(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days

print(days_between("2026-03-15", "2026-12-31"))
print(days_between("2026-03-15", "2026-03-01"))

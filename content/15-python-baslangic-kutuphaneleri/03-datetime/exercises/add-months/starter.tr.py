import calendar
from datetime import date


def add_months(text, n):
    d = date.fromisoformat(text)
    # aylari 0'dan say: d.month - 1 + n
    return text

print(add_months("2026-01-31", 1))
print(add_months("2026-11-15", 3))
print(add_months("2026-03-31", -1))

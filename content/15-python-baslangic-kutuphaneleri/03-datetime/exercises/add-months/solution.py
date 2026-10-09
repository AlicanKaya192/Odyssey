import calendar
from datetime import date


def add_months(text, n):
    d = date.fromisoformat(text)
    month_index = d.month - 1 + n
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    last = calendar.monthrange(year, month)[1]
    return date(year, month, min(d.day, last)).isoformat()

print(add_months("2026-01-31", 1))
print(add_months("2026-11-15", 3))
print(add_months("2026-03-31", -1))

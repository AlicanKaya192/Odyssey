import re
from datetime import datetime


def read_numeric(day_month, policy):
    a, b, year = [int(x) for x in day_month.split("/")]
    if policy == "US":
        month, day = a, b
    elif policy == "day-first":
        day, month = a, b
    elif a <= 12 and b <= 12 and a != b:
        return "needs_clarification"
    else:
        day, month = (a, b) if a > 12 else (b, a)
    try:
        return datetime(year, month, day).date().isoformat()
    except ValueError:
        return "rejected"


def dates_in(text, policy):
    found = re.findall(r"\b\d{2}/\d{2}/\d{4}\b", text)
    return [read_numeric(d, policy) for d in found]

TEXT = "Ordered 03/04/2026, delivered 13/04/2026."
print(dates_in(TEXT, "US"))
print(dates_in(TEXT, None))

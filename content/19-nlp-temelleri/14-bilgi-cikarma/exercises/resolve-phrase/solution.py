import re
from datetime import datetime, timedelta

PATTERN = r"(today|tomorrow|in (\d+) days) at (\d{1,2})(am|pm)?"


def resolve(phrase, reference):
    now = datetime.fromisoformat(reference)
    m = re.fullmatch(PATTERN, phrase.lower().strip())
    if m is None:
        return "rejected"
    if m[4] is None:
        return "needs_clarification"
    hour = int(m[3])
    if not 1 <= hour <= 12:
        return "rejected"
    hour = hour % 12 + (12 if m[4] == "pm" else 0)
    if m[1] == "today":
        days = 0
    elif m[1] == "tomorrow":
        days = 1
    else:
        days = int(m[2])
    day = now.date() + timedelta(days=days)
    when = datetime(day.year, day.month, day.day, hour, tzinfo=now.tzinfo)
    return when.isoformat()

REF = "2026-03-14T01:30:00+03:00"
print(resolve("in 2 days at 9am", REF))
print(resolve("Tomorrow at 12am", REF))
print(resolve("tomorrow at 7", REF))
print(resolve("next friday at 5pm", REF))

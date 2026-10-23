import json
import re
from datetime import datetime, timedelta

PHRASE = r"(today|tomorrow) at (\d{1,2})(am|pm)?"
KEYS = {"date", "time", "source"}


def check_callback(message, reply, now):
    try:
        data = json.loads(reply)
    except json.JSONDecodeError:
        return "rejected"
    if not isinstance(data, dict) or set(data) != KEYS:
        return "rejected"
    source = str(data["source"]).lower()
    m = re.fullmatch(PHRASE, source)
    if m is None or source not in message.lower():
        return "rejected"
    if m[3] is None:
        return "needs_clarification"
    if not 1 <= int(m[2]) <= 12:
        return "rejected"
    hour = int(m[2]) % 12 + (12 if m[3] == "pm" else 0)
    days = 1 if m[1] == "tomorrow" else 0
    day = datetime.fromisoformat(now).date() + timedelta(days=days)
    if (data["date"], data["time"]) != (day.isoformat(), f"{hour:02d}:00"):
        return "rejected"
    return "accepted"


NOW = "2026-03-14T01:30:00+03:00"
GOOD = ('{"date": "2026-03-15", "time": "19:00", '
        '"source": "tomorrow at 7pm"}')
VAGUE = ('{"date": "2026-03-15", "time": "07:00", '
         '"source": "tomorrow at 7"}')
print(check_callback("Call me tomorrow at 7pm.", GOOD, NOW))
print(check_callback("Call me tomorrow at 7.", VAGUE, NOW))
print(check_callback("Call me tomorrow at 7pm.", "Sure, 7pm!", NOW))

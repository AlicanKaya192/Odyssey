import json
import re
from datetime import datetime, timedelta


def check_callback(message, reply, now):
    return "accepted"


NOW = "2026-03-14T01:30:00+03:00"
GOOD = ('{"date": "2026-03-15", "time": "19:00", '
        '"source": "tomorrow at 7pm"}')
VAGUE = ('{"date": "2026-03-15", "time": "07:00", '
         '"source": "tomorrow at 7"}')
print(check_callback("Call me tomorrow at 7pm.", GOOD, NOW))
print(check_callback("Call me tomorrow at 7.", VAGUE, NOW))
print(check_callback("Call me tomorrow at 7pm.", "Sure, 7pm!", NOW))

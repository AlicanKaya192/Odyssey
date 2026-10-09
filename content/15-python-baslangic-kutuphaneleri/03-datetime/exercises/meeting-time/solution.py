from datetime import datetime
from zoneinfo import ZoneInfo


def meeting_time(local, from_zone, to_zone):
    moment = datetime.strptime(local, "%Y-%m-%d %H:%M")
    moment = moment.replace(tzinfo=ZoneInfo(from_zone))
    return moment.astimezone(ZoneInfo(to_zone)).strftime("%H:%M")

print(meeting_time("2026-03-15 14:30", "Europe/Istanbul", "America/New_York"))
print(meeting_time("2026-07-01 09:00", "Europe/London", "Asia/Tokyo"))

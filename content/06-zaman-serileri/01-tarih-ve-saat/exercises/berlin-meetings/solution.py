from datetime import datetime, timezone
from zoneinfo import ZoneInfo

berlin = ZoneInfo("Europe/Berlin")
istanbul = ZoneInfo("Europe/Istanbul")

before = datetime(2024, 3, 30, 9, 0, tzinfo=berlin)
after = datetime(2024, 3, 31, 9, 0, tzinfo=berlin)
print(before.astimezone(istanbul).strftime("%H:%M"))
print(after.astimezone(istanbul).strftime("%H:%M"))

noon_before = datetime(2024, 3, 30, 12, 0, tzinfo=berlin)
noon_after = datetime(2024, 3, 31, 12, 0, tzinfo=berlin)
gap = noon_after.astimezone(timezone.utc) - noon_before.astimezone(timezone.utc)
print(gap.total_seconds() / 3600)

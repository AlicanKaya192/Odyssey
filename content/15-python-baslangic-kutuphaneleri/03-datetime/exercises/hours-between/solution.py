from datetime import datetime

FMT = "%Y-%m-%d %H:%M"


def hours_between(start, end):
    gap = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
    return round(gap.total_seconds() / 3600, 2)

print(hours_between("2026-03-15 14:30", "2026-03-16 09:00"))
print(hours_between("2026-03-15 08:00", "2026-03-18 20:15"))

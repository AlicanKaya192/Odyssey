from datetime import date


def gfs_keep(dates, today):
    now = date.fromisoformat(today)
    kept = []
    for text in dates:
        day = date.fromisoformat(text)
        age = (now - day).days
        if age < 7:
            kept.append(text)
    return sorted(kept)

from datetime import date, timedelta

TODAY = date(2026, 11, 1)
DATES = [(TODAY - timedelta(days=i)).isoformat() for i in range(60)]
kept = gfs_keep(DATES, TODAY.isoformat())
print(len(kept))
for day in kept[:5]:
    print(day)

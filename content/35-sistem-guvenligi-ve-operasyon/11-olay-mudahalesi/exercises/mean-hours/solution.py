from datetime import datetime


def mean_hours(pairs):
    if not pairs:
        return 0.0
    total = 0
    for start, end in pairs:
        delta = datetime.fromisoformat(end) - datetime.fromisoformat(start)
        total += delta.total_seconds() / 3600
    return round(total / len(pairs), 1)

PAIRS = [
    ["2026-10-03T08:00", "2026-10-03T11:30"],
    ["2026-10-12T22:10", "2026-10-13T06:40"],
    ["2026-10-25T13:00", "2026-10-25T13:20"],
]
print(mean_hours(PAIRS))
print(mean_hours([]))

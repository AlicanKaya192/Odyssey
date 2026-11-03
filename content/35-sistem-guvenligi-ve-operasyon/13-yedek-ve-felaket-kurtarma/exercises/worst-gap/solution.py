from datetime import datetime


def worst_gap_hours(times):
    if len(times) < 2:
        return 0.0
    parsed = [datetime.fromisoformat(t) for t in times]
    gaps = [(b - a).total_seconds() / 3600 for a, b in zip(parsed, parsed[1:])]
    return round(max(gaps), 1)

TIMES = [
    "2026-11-01T00:00",
    "2026-11-01T06:00",
    "2026-11-01T12:00",
    "2026-11-02T00:00",
]
print(worst_gap_hours(TIMES))
print(worst_gap_hours(["2026-11-01T00:00"]))

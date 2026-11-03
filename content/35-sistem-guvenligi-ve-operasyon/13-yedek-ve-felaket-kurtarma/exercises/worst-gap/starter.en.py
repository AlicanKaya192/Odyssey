from datetime import datetime


def worst_gap_hours(times):
    # consecutive pairs: zip(t, t[1:])
    return 0.0

TIMES = [
    "2026-11-01T00:00",
    "2026-11-01T06:00",
    "2026-11-01T12:00",
    "2026-11-02T00:00",
]
print(worst_gap_hours(TIMES))
print(worst_gap_hours(["2026-11-01T00:00"]))

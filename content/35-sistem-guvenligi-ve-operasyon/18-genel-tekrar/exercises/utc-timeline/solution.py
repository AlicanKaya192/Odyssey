from datetime import datetime, timezone


def utc_timeline(events):
    rows = []
    for stamp, source, text in events:
        when = datetime.fromisoformat(stamp).astimezone(timezone.utc)
        rows.append((when, source, text))
    rows.sort()
    return [f"{when:%H:%M:%S} {source} {text}" for when, source, text in rows]

EVENTS = [
    ["2026-11-02T12:00:10+03:00", "web", "login"],
    ["2026-11-02T09:00:05Z", "fw", "block"],
    ["2026-11-02T09:00:20+00:00", "db", "query"],
    ["2026-11-02T10:00:05+01:00", "auth", "reset"],
]
for line in utc_timeline(EVENTS):
    print(line)

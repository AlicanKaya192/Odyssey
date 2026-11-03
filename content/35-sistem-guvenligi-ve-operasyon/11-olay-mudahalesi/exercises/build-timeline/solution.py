from datetime import datetime, timezone


def build_timeline(sources):
    events = []
    for source, items in sources.items():
        for stamp, text in items:
            when = datetime.fromisoformat(stamp).astimezone(timezone.utc)
            events.append((when, source, text))
    return [f"{w.strftime('%H:%M:%S')} {s} {t}" for w, s, t in sorted(events)]

SOURCES = {
    "vpn": [["2026-11-01T02:14:00+00:00", "login bob"]],
    "web": [["2026-11-01T05:16:30+03:00", "admin page"]],
    "db": [
        ["2026-11-01T02:20:05+00:00", "table exported"],
        ["2026-11-01T02:15:10+00:00", "new db user"],
    ],
}
for line in build_timeline(SOURCES):
    print(line)

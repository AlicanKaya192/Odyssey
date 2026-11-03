def build_timeline(sources):
    lines = []
    for source, items in sources.items():
        for stamp, text in items:
            lines.append(stamp[11:19] + " " + source + " " + text)
    return sorted(lines)

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

def utc_order(events):
    return [text for stamp, text in sorted(events)]

EVENTS = [
    ["2026-11-01T09:59:59+03:00", "file deleted"],
    ["2026-11-01T07:00:02+00:00", "login from new place"],
    ["2026-11-01T08:00:04+01:00", "admin group changed"],
]
for text in utc_order(EVENTS):
    print(text)

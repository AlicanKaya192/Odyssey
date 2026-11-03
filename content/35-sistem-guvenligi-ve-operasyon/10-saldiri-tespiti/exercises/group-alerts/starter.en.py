def group_alerts(alerts, gap):
    lines = []
    # sort by source and time, then group
    return lines

ALERTS = [
    [10, "203.0.113.9"],
    [12, "203.0.113.9"],
    [30, "198.51.100.4"],
    [15, "203.0.113.9"],
    [90, "203.0.113.9"],
]
for line in group_alerts(ALERTS, 10):
    print(line)

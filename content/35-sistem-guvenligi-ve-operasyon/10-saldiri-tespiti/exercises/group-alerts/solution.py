def group_alerts(alerts, gap):
    groups = []
    for second, source in sorted(alerts, key=lambda a: (a[1], a[0])):
        last = groups[-1] if groups else None
        if last and last[0] == source and second - last[2] <= gap:
            last[2] = second
            last[3] += 1
        else:
            groups.append([source, second, second, 1])
    return [f"{s} {first}-{end} ({n})" for s, first, end, n in groups]

ALERTS = [
    [10, "203.0.113.9"],
    [12, "203.0.113.9"],
    [30, "198.51.100.4"],
    [15, "203.0.113.9"],
    [90, "203.0.113.9"],
]
for line in group_alerts(ALERTS, 10):
    print(line)

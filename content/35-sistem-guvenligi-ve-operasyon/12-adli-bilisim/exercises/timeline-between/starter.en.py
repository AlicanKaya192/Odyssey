def timeline_between(records, start, end):
    lines = []
    for path, kind, time in records:
        lines.append(f"{time} {kind} {path}")
    return sorted(lines)

RECORDS = [
    ["/tmp/x.zip", "created", "02:17:40"],
    ["/srv/data/customers.csv", "accessed", "02:19:58"],
    ["/tmp/x.zip", "modified", "02:20:03"],
    ["/var/log/auth.log", "modified", "01:05:00"],
    ["/home/bob/.bash_history", "modified", "02:21:10"],
]
for line in timeline_between(RECORDS, "02:18:00", "02:21:00"):
    print(line)

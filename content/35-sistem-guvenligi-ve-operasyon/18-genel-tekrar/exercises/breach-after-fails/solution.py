from collections import Counter


def breaches(lines, limit):
    fails = Counter()
    found = set()
    for line in lines:
        _, status, *pairs = line.split()
        ip = dict(pair.split("=", 1) for pair in pairs)["ip"]
        if status == "FAIL":
            fails[ip] += 1
        elif status == "OK" and fails[ip] >= limit:
            found.add(ip)
    return sorted(found)

LOG = [
    "2026-11-02T09:00:05 FAIL user=ada ip=10.0.0.7",
    "2026-11-02T09:00:09 FAIL user=ada ip=10.0.0.7",
    "2026-11-02T09:00:12 FAIL user=root ip=10.0.0.7",
    "2026-11-02T09:00:15 OK user=ada ip=10.0.0.7",
    "2026-11-02T09:01:00 FAIL user=bob ip=10.0.0.9",
    "2026-11-02T09:01:02 FAIL user=bob ip=10.0.0.9",
    "2026-11-02T09:01:04 FAIL user=bob ip=10.0.0.9",
    "2026-11-02T09:02:00 OK user=eve ip=10.0.0.4",
    "2026-11-02T09:02:30 FAIL user=eve ip=10.0.0.4",
]
print(breaches(LOG, 3))
print(breaches(LOG, 4))

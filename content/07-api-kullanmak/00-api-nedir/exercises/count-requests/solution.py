log = [
    ("app", "/weather"),
    ("web", "/weather"),
    ("app", "/cities"),
    ("bot", "/news"),
    ("app", "/weather"),
    ("web", "/forecast"),
    ("bot", "/news"),
    ("app", "/forecast"),
]
known = ["/weather", "/forecast", "/cities"]

counts = {}
for client, path in log:
    counts[path] = counts.get(path, 0) + 1

for path in sorted(counts):
    print(path, counts[path])

missing = 0
for path in counts:
    if path not in known:
        missing += counts[path]
print("404 responses:", missing)

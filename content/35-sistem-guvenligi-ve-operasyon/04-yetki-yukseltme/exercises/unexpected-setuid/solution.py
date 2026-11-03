def unexpected_setuid(files, allowed):
    found = []
    for f in files:
        if f["mode"] & 0o4000 and f["path"] not in allowed:
            found.append(f["path"])
    return sorted(found)

FILES = [
    {"path": "/usr/bin/passwd", "mode": 0o4755},
    {"path": "/opt/tools/report-tool", "mode": 0o4755},
    {"path": "/usr/bin/ls", "mode": 0o755},
    {"path": "/opt/app/helper", "mode": 0o4711},
]
for path in unexpected_setuid(FILES, ["/usr/bin/passwd"]):
    print(path)

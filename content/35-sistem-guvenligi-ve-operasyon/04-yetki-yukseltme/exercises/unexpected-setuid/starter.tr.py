def unexpected_setuid(files, allowed):
    found = []
    # setuid biti 0o4000
    return found

FILES = [
    {"path": "/usr/bin/passwd", "mode": 0o4755},
    {"path": "/opt/tools/report-tool", "mode": 0o4755},
    {"path": "/usr/bin/ls", "mode": 0o755},
    {"path": "/opt/app/helper", "mode": 0o4711},
]
for path in unexpected_setuid(FILES, ["/usr/bin/passwd"]):
    print(path)

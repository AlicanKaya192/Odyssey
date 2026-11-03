def audit_files(files):
    lines = []
    for f in files:
        if f["mode"] & 0o002:
            lines.append(f["path"] + ": world-writable")
    return lines

FILES = [
    {"path": "/srv/app/run.sh", "mode": 0o755, "secret": False},
    {"path": "/srv/app/config.ini", "mode": 0o666, "secret": False},
    {"path": "/home/ada/.env", "mode": 0o640, "secret": True},
    {"path": "/tmp/notes.txt", "mode": 0o777, "secret": True},
    {"path": "/home/ada/id_key", "mode": 0o600, "secret": True},
]
for line in audit_files(FILES):
    print(line)

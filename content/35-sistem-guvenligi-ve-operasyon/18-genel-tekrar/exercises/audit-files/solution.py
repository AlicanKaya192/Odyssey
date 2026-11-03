SECRET_KEYS = ("password=", "api_key=", "token=")


def audit_files(files):
    findings = []
    for path, mode, content in files:
        if int(mode[-1]) & 2:
            findings.append(path + ": world-writable")
        for line in content.splitlines():
            if line.strip().lower().startswith(SECRET_KEYS):
                findings.append(path + ": secret")
                break
    return sorted(findings)

FILES = [
    ["app/config.ini", "640", "debug=false\npassword=hunter2\n"],
    ["app/run.sh", "755", "echo start\n"],
    ["tmp/notes.txt", "666", "API_KEY=abc123\n"],
    ["web/index.html", "644", "<p>password=</p>\n"],
]
for finding in audit_files(FILES):
    print(finding)

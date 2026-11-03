SECRET_KEYS = ("password=", "api_key=", "token=")


def audit_files(files):
    findings = []
    for path, mode, content in files:
        if mode == "777":
            findings.append(path + ": world-writable")
        if "password=" in content:
            findings.append(path + ": secret")
    return sorted(findings)

FILES = [
    ["app/config.ini", "640", "debug=false\npassword=hunter2\n"],
    ["app/run.sh", "755", "echo start\n"],
    ["tmp/notes.txt", "666", "API_KEY=abc123\n"],
    ["web/index.html", "644", "<p>password=</p>\n"],
]
for finding in audit_files(FILES):
    print(finding)

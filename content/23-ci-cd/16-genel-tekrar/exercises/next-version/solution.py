def next_version(current, commits):
    major, minor, patch = (int(part) for part in current.split("."))
    level = 0
    for message in commits:
        head = message.split(":")[0]
        kind = head.split("(")[0].rstrip("!")
        if head.endswith("!") or "BREAKING CHANGE" in message:
            level = max(level, 3)
        elif kind == "feat":
            level = max(level, 2)
        elif kind == "fix":
            level = max(level, 1)
    if level == 3:
        return f"{major + 1}.0.0"
    if level == 2:
        return f"{major}.{minor + 1}.0"
    if level == 1:
        return f"{major}.{minor}.{patch + 1}"
    return None


print(next_version("1.4.2", ["fix: handle empty cart", "docs: typo"]))
print(next_version("1.4.2", ["fix: a", "feat(api): add search"]))
print(next_version("1.4.2", ["feat!: drop old routes", "fix: b"]))
print(next_version("1.4.2", ["chore: bump deps"]))

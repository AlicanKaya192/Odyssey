import hashlib


def duplicates(paths):
    groups = {}
    for path in paths:
        with open(path, "rb") as file:
            digest = hashlib.file_digest(file, "sha256").hexdigest()
        groups.setdefault(digest, []).append(path)
    found = [sorted(group) for group in groups.values() if len(group) > 1]
    return sorted(found)

for group in duplicates(["files/a.txt", "files/b.txt", "files/c.txt", "files/d.txt"]):
    print(group)

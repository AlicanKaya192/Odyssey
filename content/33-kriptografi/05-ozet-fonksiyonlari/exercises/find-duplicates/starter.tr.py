import hashlib


def find_duplicates(items):
    groups = {}
    for name, content in items.items():
        digest = hashlib.sha256(content.encode()).hexdigest()
        groups.setdefault(digest, []).append(name)
    return list(groups.values())

items = {"x": "hello", "y": "world", "z": "hello", "w": "world", "v": "unique"}
for group in find_duplicates(items):
    print(group)

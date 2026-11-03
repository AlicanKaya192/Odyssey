import hashlib


def find_duplicates(items):
    groups = {}
    for name, content in items.items():
        digest = hashlib.sha256(content.encode()).hexdigest()
        groups.setdefault(digest, []).append(name)
    result = [sorted(names) for names in groups.values() if len(names) > 1]
    return sorted(result)

items = {"x": "hello", "y": "world", "z": "hello", "w": "world", "v": "unique"}
for group in find_duplicates(items):
    print(group)

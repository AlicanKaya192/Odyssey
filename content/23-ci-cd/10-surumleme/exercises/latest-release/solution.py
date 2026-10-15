def latest_release(tags):
    best = None
    best_key = None
    for tag in tags:
        if not tag.startswith("v"):
            continue
        parts = tag[1:].split(".")
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            continue
        key = tuple(int(part) for part in parts)
        if best_key is None or key > best_key:
            best = tag
            best_key = key
    return best


tags = ["v1.2.0", "v1.10.0", "nightly", "v1.9.3", "v2.0.0rc1", "v1.10"]
print(latest_release(tags))
print(latest_release(["docs", "v0.1.0-beta"]))
print(latest_release(["v0.9.12", "v0.10.0"]))

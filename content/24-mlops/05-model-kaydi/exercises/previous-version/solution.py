def previous_version(history, alias):
    versions = [version for name, version in history if name == alias]
    current = versions[-1] if versions else None
    for version in reversed(versions):
        if version != current:
            return version
    return None


history = [
    ["production", 1],
    ["staging", 2],
    ["production", 3],
    ["staging", 4],
]
print(previous_version(history, "production"))
print(previous_version(history, "staging"))
print(previous_version([["production", 1]], "production"))

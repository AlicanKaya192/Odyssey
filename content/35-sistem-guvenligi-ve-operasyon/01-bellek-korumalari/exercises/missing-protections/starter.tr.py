REQUIRED = ["canary", "nx", "pie"]


def missing_protections(binary):
    missing = []
    for name in REQUIRED:
        if binary[name] is False:
            missing.append(name)
    return missing

BINARIES = [
    {"name": "app", "canary": True, "nx": True, "pie": True},
    {"name": "tool", "canary": False, "nx": True},
    {"name": "old", "nx": False},
]
for binary in BINARIES:
    missing = missing_protections(binary)
    print(binary["name"] + ":", ", ".join(missing) or "ok")

def version(text):
    return tuple(int(part) for part in text.split("."))


def affected(installed, advisories):
    lines = []
    for name, introduced, fixed, adv in advisories:
        if name not in installed:
            continue
        v = version(installed[name])
        if version(introduced) <= v < version(fixed):
            lines.append(f"{name} {installed[name]}: {adv}")
    return sorted(lines)

INSTALLED = {"web": "2.3.1", "http": "1.10.0", "pool": "0.4.2"}
ADVISORIES = [
    ["web", "2.0.0", "2.3.2", "ADV-1"],
    ["http", "1.0.0", "1.9.0", "ADV-2"],
    ["pool", "0.1.0", "0.5.0", "ADV-3"],
    ["cache", "1.0.0", "1.2.0", "ADV-4"],
]
for line in affected(INSTALLED, ADVISORIES):
    print(line)

def matches(combo, rule):
    for key, value in rule.items():
        if combo.get(key) != value:
            return False
    return True


def apply_exclude(combos, exclude):
    kept = []
    for combo in combos:
        removed = False
        for rule in exclude:
            if matches(combo, rule):
                removed = True
        if not removed:
            kept.append(combo)
    return kept


combos = [
    {"os": "ubuntu-latest", "python": "3.12"},
    {"os": "ubuntu-latest", "python": "3.13"},
    {"os": "windows-latest", "python": "3.12"},
    {"os": "windows-latest", "python": "3.13"},
]
for combo in apply_exclude(combos, [{"os": "windows-latest", "python": "3.12"}]):
    print(combo)
print(len(apply_exclude(combos, [{"os": "windows-latest"}])))

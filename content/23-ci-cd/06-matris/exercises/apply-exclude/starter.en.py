def apply_exclude(combos, exclude):
    # Keep the ones that match no rule.
    pass


combos = [
    {"os": "ubuntu-latest", "python": "3.12"},
    {"os": "ubuntu-latest", "python": "3.13"},
    {"os": "windows-latest", "python": "3.12"},
    {"os": "windows-latest", "python": "3.13"},
]
for combo in apply_exclude(combos, [{"os": "windows-latest", "python": "3.12"}]):
    print(combo)
print(len(apply_exclude(combos, [{"os": "windows-latest"}])))

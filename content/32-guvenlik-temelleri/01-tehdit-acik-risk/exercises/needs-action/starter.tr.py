def needs_action(findings, threshold):
    selected = []
    # yamasiz ve esigi gecenleri sec, sonra sirala
    return [f["name"] for f in selected]

findings = [
    {"name": "web login", "score": 7.5, "exposed": True, "patched": False},
    {"name": "old library", "score": 9.8, "exposed": False, "patched": False},
    {"name": "report tool", "score": 8.1, "exposed": True, "patched": True},
    {"name": "api server", "score": 9.1, "exposed": True, "patched": False},
    {"name": "test box", "score": 4.3, "exposed": False, "patched": False},
]
for threshold in [7.0, 4.0]:
    print("threshold", threshold)
    for name in needs_action(findings, threshold):
        print(" ", name)

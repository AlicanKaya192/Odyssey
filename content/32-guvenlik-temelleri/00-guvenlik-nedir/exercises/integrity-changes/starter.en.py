def integrity_changes(old, new):
    report = {"added": [], "removed": [], "changed": []}
    # compare the two dictionaries
    return report

old = {"app.py": "1f3a", "config.ini": "77b0", "notes.txt": "a210"}
new = {"app.py": "1f3a", "config.ini": "9c4e", "run.sh": "0d5e"}
report = integrity_changes(old, new)
for kind in ["added", "removed", "changed"]:
    print(kind, report[kind])

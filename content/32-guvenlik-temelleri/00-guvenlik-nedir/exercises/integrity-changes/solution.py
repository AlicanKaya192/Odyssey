def integrity_changes(old, new):
    added = [name for name in new if name not in old]
    removed = [name for name in old if name not in new]
    changed = [name for name in old if name in new and old[name] != new[name]]
    return {"added": sorted(added), "removed": sorted(removed), "changed": sorted(changed)}

old = {"app.py": "1f3a", "config.ini": "77b0", "notes.txt": "a210"}
new = {"app.py": "1f3a", "config.ini": "9c4e", "run.sh": "0d5e"}
report = integrity_changes(old, new)
for kind in ["added", "removed", "changed"]:
    print(kind, report[kind])

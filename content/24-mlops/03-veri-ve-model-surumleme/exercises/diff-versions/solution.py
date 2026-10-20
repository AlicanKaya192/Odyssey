def diff_versions(old, new):
    old_rows = {row["id"]: row for row in old}
    new_rows = {row["id"]: row for row in new}
    added = [i for i in new_rows if i not in old_rows]
    removed = [i for i in old_rows if i not in new_rows]
    changed = [i for i in old_rows if i in new_rows and old_rows[i] != new_rows[i]]
    return {"added": sorted(added), "removed": sorted(removed), "changed": sorted(changed)}


old = [{"id": "C1", "plan": "basic"}, {"id": "C2", "plan": "pro"}, {"id": "C3", "plan": "pro"}]
new = [{"id": "C3", "plan": "pro"}, {"id": "C2", "plan": "basic"}, {"id": "C4", "plan": "pro"}]
for key, ids in diff_versions(old, new).items():
    print(key, ids)

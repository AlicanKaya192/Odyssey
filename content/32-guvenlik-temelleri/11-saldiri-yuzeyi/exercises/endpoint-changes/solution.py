def endpoint_changes(old, new):
    old_set, new_set = set(old), set(new)
    return {"added": sorted(new_set - old_set), "removed": sorted(old_set - new_set)}

v1 = ["/login", "/search", "/admin", "/old"]
v2 = ["/login", "/search", "/admin", "/export", "/debug"]
report = endpoint_changes(v1, v2)
print("added", report["added"])
print("removed", report["removed"])

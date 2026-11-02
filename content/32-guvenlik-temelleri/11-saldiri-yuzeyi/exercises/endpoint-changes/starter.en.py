def endpoint_changes(old, new):
    added = [path for path in new if path not in old]
    return {"added": added, "removed": []}

v1 = ["/login", "/search", "/admin", "/old"]
v2 = ["/login", "/search", "/admin", "/export", "/debug"]
report = endpoint_changes(v1, v2)
print("added", report["added"])
print("removed", report["removed"])

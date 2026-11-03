def wx_violations(regions):
    found = []
    for name, perms in regions.items():
        if "w" in perms and "x" in perms:
            found.append(name)
    return sorted(found)

REGIONS = {
    "code": "r-x",
    "data": "rw-",
    "stack": "rw-",
    "jit": "rwx",
    "plugin": "-wx",
}
print(wx_violations(REGIONS))

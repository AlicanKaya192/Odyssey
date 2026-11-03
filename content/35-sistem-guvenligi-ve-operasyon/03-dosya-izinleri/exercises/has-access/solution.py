def has_access(file, user, groups, action):
    bit = {"r": 4, "w": 2, "x": 1}[action]
    mode = file["mode"]
    if user == file["owner"]:
        bits = (mode >> 6) & 7
    elif file["group"] in groups:
        bits = (mode >> 3) & 7
    else:
        bits = mode & 7
    return bool(bits & bit)

secret = {"owner": "ada", "group": "staff", "mode": 0o077}
report = {"owner": "ada", "group": "staff", "mode": 0o640}
print(has_access(secret, "ada", ["staff"], "r"))
print(has_access(secret, "bob", ["staff"], "r"))
print(has_access(report, "ada", [], "w"))
print(has_access(report, "bob", ["staff"], "w"))
print(has_access(report, "eve", ["guests"], "r"))

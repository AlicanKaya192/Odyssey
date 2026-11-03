def has_access(file, user, groups, action):
    bit = {"r": 4, "w": 2, "x": 1}[action]
    mode = file["mode"]
    for shift in (6, 3, 0):
        if (mode >> shift) & bit:
            return True
    return False

secret = {"owner": "ada", "group": "staff", "mode": 0o077}
report = {"owner": "ada", "group": "staff", "mode": 0o640}
print(has_access(secret, "ada", ["staff"], "r"))
print(has_access(secret, "bob", ["staff"], "r"))
print(has_access(report, "ada", [], "w"))
print(has_access(report, "bob", ["staff"], "w"))
print(has_access(report, "eve", ["guests"], "r"))

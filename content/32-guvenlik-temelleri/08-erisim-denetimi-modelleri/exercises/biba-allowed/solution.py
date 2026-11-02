LEVELS = ["low", "medium", "high"]


def biba_allowed(subject, obj, action):
    s, o = LEVELS.index(subject), LEVELS.index(obj)
    if action == "read":
        return s <= o
    if action == "write":
        return s >= o
    return False

for subject, obj in [("medium", "low"), ("medium", "high"), ("high", "high")]:
    print(subject, obj, biba_allowed(subject, obj, "read"), biba_allowed(subject, obj, "write"))
print(biba_allowed("low", "low", "delete"))

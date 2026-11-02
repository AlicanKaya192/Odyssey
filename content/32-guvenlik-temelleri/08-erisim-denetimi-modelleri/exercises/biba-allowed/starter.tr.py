LEVELS = ["low", "medium", "high"]


def biba_allowed(subject, obj, action):
    s, o = LEVELS.index(subject), LEVELS.index(obj)
    return s >= o if action == "read" else s <= o

for subject, obj in [("medium", "low"), ("medium", "high"), ("high", "high")]:
    print(subject, obj, biba_allowed(subject, obj, "read"), biba_allowed(subject, obj, "write"))
print(biba_allowed("low", "low", "delete"))

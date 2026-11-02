def count_pillars(incidents):
    counts = {"C": 0, "I": 0, "A": 0}
    # look at every incident and count the broken legs
    return counts

incidents = [
    {"leaked": True, "modified": False, "unreachable": False},
    {"leaked": False, "modified": True, "unreachable": True},
    {"leaked": True, "modified": True, "unreachable": True},
    {"leaked": False, "modified": False, "unreachable": True},
]
print(count_pillars(incidents))

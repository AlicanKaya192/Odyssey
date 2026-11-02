def count_pillars(incidents):
    counts = {"C": 0, "I": 0, "A": 0}
    for incident in incidents:
        if incident["leaked"]:
            counts["C"] += 1
        if incident["modified"]:
            counts["I"] += 1
        if incident["unreachable"]:
            counts["A"] += 1
    return counts

incidents = [
    {"leaked": True, "modified": False, "unreachable": False},
    {"leaked": False, "modified": True, "unreachable": True},
    {"leaked": True, "modified": True, "unreachable": True},
    {"leaked": False, "modified": False, "unreachable": True},
]
print(count_pillars(incidents))

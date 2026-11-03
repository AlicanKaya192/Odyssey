def custody_gaps(entries):
    gaps = []
    holder = None
    for time, giver, taker in entries:
        if holder is not None and giver != holder:
            gaps.append(time)
        holder = taker
    return gaps

CUSTODY = [
    ["02:40", "ada", "locker"],
    ["09:15", "locker", "eve"],
    ["17:00", "joe", "locker"],
    ["18:30", "locker", "eve"],
    ["19:00", "bob", "locker"],
]
print(custody_gaps(CUSTODY))

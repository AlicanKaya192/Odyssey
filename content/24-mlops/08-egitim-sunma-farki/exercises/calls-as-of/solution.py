def calls_as_of(labels, calls):
    result = []
    for customer, day in labels:
        count = sum(1 for who, when in calls if who == customer and when < day)
        result.append([customer, day, count])
    return result


labels = [["C1", "2026-02-15"], ["C2", "2026-02-15"], ["C1", "2026-03-10"]]
calls = [["C1", "2026-01-20"], ["C1", "2026-02-15"], ["C1", "2026-03-01"], ["C2", "2026-04-01"]]
for row in calls_as_of(labels, calls):
    print(row)

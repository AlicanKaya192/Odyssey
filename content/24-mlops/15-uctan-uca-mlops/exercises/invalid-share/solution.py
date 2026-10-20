def invalid_share(rows, limits):
    bad = 0
    for row in rows:
        for name, (low, high) in limits.items():
            value = row.get(name)
            if value is None or not low <= value <= high:
                bad += 1
                break
    return round(bad / len(rows), 3)


limits = {"fee": [5, 100], "calls": [0, 10]}
rows = [{"fee": 30, "calls": 2}, {"fee": 3000, "calls": 1},
        {"fee": 40}, {"fee": 50, "calls": 11}]
print(invalid_share(rows, limits))
print(invalid_share(rows[:1], limits))

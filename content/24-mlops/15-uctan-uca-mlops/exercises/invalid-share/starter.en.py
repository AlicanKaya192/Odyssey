def invalid_share(rows, limits):
    # One problem in a row is enough.
    pass


limits = {"fee": [5, 100], "calls": [0, 10]}
rows = [{"fee": 30, "calls": 2}, {"fee": 3000, "calls": 1},
        {"fee": 40}, {"fee": 50, "calls": 11}]
print(invalid_share(rows, limits))
print(invalid_share(rows[:1], limits))

def calls_as_of(labels, calls):
    # For every label, count the same customer's earlier calls.
    pass


labels = [["C1", "2026-02-15"], ["C2", "2026-02-15"], ["C1", "2026-03-10"]]
calls = [["C1", "2026-01-20"], ["C1", "2026-02-15"], ["C1", "2026-03-01"], ["C2", "2026-04-01"]]
for row in calls_as_of(labels, calls):
    print(row)

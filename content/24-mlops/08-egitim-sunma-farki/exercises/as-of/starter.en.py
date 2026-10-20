def as_of(history, day):
    # Walk the sorted list, keep the last value whose date isn't past.
    pass


history = [["2026-01-01", 0], ["2026-02-01", 1], ["2026-03-01", 4]]
print(as_of(history, "2026-02-15"))
print(as_of(history, "2026-03-01"))
print(as_of(history, "2025-12-31"))
print(as_of([], "2026-01-01"))

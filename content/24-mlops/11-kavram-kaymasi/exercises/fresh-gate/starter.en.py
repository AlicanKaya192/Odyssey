def fresh_gate(sets, now, max_age, min_gain):
    # First pick the current sets, then the mean gain.
    pass


sets = [
    {"month": 0, "old": 0.813, "new": 0.718},
    {"month": 5, "old": 0.681, "new": 0.837},
]
print(fresh_gate(sets, 5, 1, 0.003))
print(fresh_gate(sets[:1], 0, 1, 0.003))
print(fresh_gate(sets, 9, 1, 0.003))

def fresh_gate(sets, now, max_age, min_gain):
    fresh = [s for s in sets if now - s["month"] <= max_age]
    if not fresh:
        return ["no fresh set", 0]
    gain = round(sum(s["new"] - s["old"] for s in fresh) / len(fresh), 3)
    if gain >= min_gain:
        return ["promote", gain]
    return ["keep", gain]


sets = [
    {"month": 0, "old": 0.813, "new": 0.718},
    {"month": 5, "old": 0.681, "new": 0.837},
]
print(fresh_gate(sets, 5, 1, 0.003))
print(fresh_gate(sets[:1], 0, 1, 0.003))
print(fresh_gate(sets, 9, 1, 0.003))

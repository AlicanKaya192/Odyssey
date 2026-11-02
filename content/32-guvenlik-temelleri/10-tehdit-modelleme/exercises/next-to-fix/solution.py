def next_to_fix(threats, n):
    open_ones = [t for t in threats if t["status"] == "open"]
    open_ones.sort(key=lambda t: (-t["likelihood"] * t["impact"], t["id"]))
    return [t["id"] for t in open_ones][:n]

threats = [
    {"id": "T1", "likelihood": 4, "impact": 5, "status": "open"},
    {"id": "T2", "likelihood": 5, "impact": 4, "status": "open"},
    {"id": "T3", "likelihood": 5, "impact": 5, "status": "mitigated"},
    {"id": "T4", "likelihood": 2, "impact": 2, "status": "open"},
    {"id": "T5", "likelihood": 3, "impact": 3, "status": "accepted"},
]
print(next_to_fix(threats, 2))
print(next_to_fix(threats, 10))

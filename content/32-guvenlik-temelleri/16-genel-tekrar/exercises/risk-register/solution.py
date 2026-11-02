def level(score):
    if score <= 4:
        return "low"
    if score <= 9:
        return "medium"
    if score <= 16:
        return "high"
    return "critical"


def risk_register(threats):
    rows = []
    for t in threats:
        score = t["likelihood"] * t["impact"]
        rows.append([t["id"], t["stride"], score, level(score)])
    return sorted(rows, key=lambda r: (-r[2], r[0]))

threats = [
    {"id": "T1", "stride": "S", "likelihood": 4, "impact": 5},
    {"id": "T2", "stride": "I", "likelihood": 2, "impact": 4},
    {"id": "T3", "stride": "D", "likelihood": 3, "impact": 3},
    {"id": "T0", "stride": "E", "likelihood": 4, "impact": 5},
    {"id": "T4", "stride": "R", "likelihood": 1, "impact": 2},
]
for row in risk_register(threats):
    print(*row)

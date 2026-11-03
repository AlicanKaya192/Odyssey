from collections import Counter


def k_anonymity(rows, quasi):
    if not rows:
        return 0
    groups = Counter(tuple(row[name] for name in quasi) for row in rows)
    return min(groups.values())

ROWS = [
    {"age_band": "30-39", "area": "347**", "illness": "flu"},
    {"age_band": "30-39", "area": "347**", "illness": "asthma"},
    {"age_band": "50-59", "area": "064**", "illness": "flu"},
    {"age_band": "50-59", "area": "064**", "illness": "diabetes"},
    {"age_band": "40-49", "area": "352**", "illness": "asthma"},
]
print(k_anonymity(ROWS, ["age_band", "area"]))
print(k_anonymity(ROWS, ["age_band"]))
print(k_anonymity(ROWS, []))

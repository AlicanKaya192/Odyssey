from collections import Counter


def k_anonymity(rows, quasi):
    groups = Counter()
    # a tuple of the quasi fields for each row
    return 0

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

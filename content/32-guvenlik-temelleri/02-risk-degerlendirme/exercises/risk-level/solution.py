def risk_level(score):
    if score <= 4:
        return "low"
    if score <= 9:
        return "medium"
    if score <= 16:
        return "high"
    return "critical"

for score in [1, 4, 5, 9, 10, 16, 17, 25]:
    print(score, risk_level(score))

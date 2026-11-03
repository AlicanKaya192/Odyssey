def cvss_rating(score):
    if score == 0:
        return "none"
    if score < 4:
        return "low"
    if score < 7:
        return "medium"
    if score < 9:
        return "high"
    return "critical"

for score in [0, 3.9, 4.0, 6.9, 7.0, 8.9, 9.0, 10.0]:
    print(score, cvss_rating(score))

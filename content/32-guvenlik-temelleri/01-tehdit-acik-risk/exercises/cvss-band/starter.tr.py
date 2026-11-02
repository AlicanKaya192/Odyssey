def cvss_band(score):
    if score == 0:
        return "None"
    if score <= 4:
        return "Low"
    if score <= 7:
        return "Medium"
    if score <= 9:
        return "High"
    return "Critical"

for score in [0.0, 2.5, 4.0, 6.9, 7.0, 9.0, 10.0]:
    print(score, cvss_band(score))

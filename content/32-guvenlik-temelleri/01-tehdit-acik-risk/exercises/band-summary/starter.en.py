def cvss_band(score):
    if score == 0:
        return "None"
    if score < 4:
        return "Low"
    if score < 7:
        return "Medium"
    if score < 9:
        return "High"
    return "Critical"


def band_summary(scores):
    summary = {}
    # count the severity of every score
    return summary

summary = band_summary([9.8, 7.5, 5.3, 3.1, 0.0, 7.0, 9.1])
for band, count in summary.items():
    print(band, count)

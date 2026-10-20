def audit_codes(release, min_gain):
    codes = []
    if release["seed"] is None:
        codes.append("seed")
    if not release["data_digest"]:
        codes.append("digest")
    if release["gate_month"] < release["trained_month"]:
        codes.append("gate")
    if release["gain"] < min_gain:
        codes.append("gain")
    if release["threshold"] == 0.5:
        codes.append("threshold")
    if release["fallback"] is None:
        codes.append("fallback")
    for needed in ["drift", "calibration"]:
        if needed not in release["monitors"]:
            codes.append(needed)
    return codes


release = {"seed": None, "data_digest": "", "trained_month": 5,
           "gate_month": 0, "gain": 0.001, "threshold": 0.5,
           "fallback": None, "monitors": ["accuracy"]}
for code in audit_codes(release, 0.003):
    print(code)
good = {"seed": 7, "data_digest": "2448b83141ea", "trained_month": 5,
        "gate_month": 5, "gain": 0.01, "threshold": 0.31,
        "fallback": "rule", "monitors": ["drift", "calibration"]}
print(audit_codes(good, 0.003))
